#  This file is part of twp.
#
#  twp is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  twp is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with
#  twp. If not, see <http://www.gnu.org/licenses/>.

# TODO create a setup.py


# Tweet Parser and Formatter ---------------------------------------------------
# ------------------------------------------------------------------------------
import re
import urllib

# Some of this code has been translated from the twitter-text-java library:
# <http://github.com/mzsanford/twitter-text-java>
AT_SIGNS = ur'[@\uff20]'
UTF_CHARS = ur'a-z0-9_\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u00ff'
SPACES = ur'[\u0020\u00A0\u1680\u180E\u2002\u2003\u2004\u2005\u2006\u2007' \
            + ur'\u2008\u2009\u200A\u200B\u200C\u200D\u202F\u205F\u2060\u3000]'

# Users
USERNAME_REGEX = re.compile(ur'\B' + AT_SIGNS \
                 + ur'([a-z0-9_]{1,20})(/[a-z][a-z0-9\\x80-\\xFF-]{0,79})?',
                 re.IGNORECASE)

REPLY_REGEX = re.compile(ur'^(?:' + SPACES + ur')*' + AT_SIGNS \
              + ur'([a-z0-9_]{1,20}).*', re.IGNORECASE)

# Hashtags
HASHTAG_EXP = ur'(^|[^0-9A-Z&/]+)(#|\uff03)([0-9A-Z_]*[A-Z_]+[%s]*)' % UTF_CHARS
HASHTAG_REGEX = re.compile(HASHTAG_EXP, re.IGNORECASE)

# Lists
LIST_CHARS = ur'([^a-z0-9_]|^)(' + AT_SIGNS \
             + ur'+)([a-z0-9_]{1,20})(/[a-z][a-z0-9\\x80-\\xFF-]{0,79})?'

LIST_REGEX = re.compile(LIST_CHARS, re.IGNORECASE)

# URLs
PRE_CHARS = ur'(?:[^/"\':!=]|^|\:)'
DOMAIN_CHARS = ur'([\.-]|[^\s_\!\.])+\.[a-z]{2,}(?::[0-9]+)?'
PATH_CHARS = ur'(?:[\.,]?[%s!\*\'\(\);:=\+\$/%s#\[\]\-_,~@])' % (UTF_CHARS, '%')
QUERY_CHARS = ur'[a-z0-9!\*\'\(\);:&=\+\$/%#\[\]\-_\.,~]'

# Valid end-of-path chracters (so /foo. does not gobble the period).
# 1. Allow ) for Wikipedia URLs.
# 2. Allow =&# for empty URL parameters and other URL-join artifacts
PATH_ENDING_CHARS = ur'[%s\)=#/]' % UTF_CHARS
QUERY_ENDING_CHARS = '[a-z0-9_&=#]'

URL_REGEX = re.compile('((' + PRE_CHARS + ')((https?://|www\\.)(' \
                       + DOMAIN_CHARS + ')(/' + PATH_CHARS + '*' \
                       + PATH_ENDING_CHARS + '?)?(\\?' + QUERY_CHARS + '*' \
                       + QUERY_ENDING_CHARS + ')?))', re.IGNORECASE)


class ParseResult:
    """A class containing the results of a parsed Tweet.
    
    Attributes:
    - urls:
        A list containing all the valid urls in the Tweet.
    
    - users
        A list containing all the valid usernames in the Tweet.
    
    - reply
        A string containing the username this tweet was a reply to.
        This only matches a username at the beginning of the Tweet,
        it may however be preceeded by whitespace.
        Note: It's generally better to rely on the Tweet JSON/XML in order to 
        find out if it's a reply or not.
        
    - lists
        A list containing all the valid lists in the Tweet.
        Each list item is a tuple in the format (username, listname).
        
    - tags
        A list containing all the valid tags in theTweet.
    
    - html
        A string containg formatted HTML.
        To change the formatting sublcass twp.Parser and override the format_*
        methods.
    
    """
    
    def __init__(self, urls, users, reply, lists, tags, html):
        self.urls = urls
        self.users = users
        self.lists = lists
        self.reply = reply
        self.tags = tags
        self.html = html


class Parser:
    """A Tweet Parser"""
    
    def __init__(self, max_url_length=30):
        self._max_url_length = max_url_length
    
    def parse(self, text):
        """Parse the text and return a ParseResult instance."""
        
        # Reset
        self._urls = []
        self._users = []
        self._lists = []
        self._tags = []
        
        # Filter
        html = URL_REGEX.sub(self._parse_urls, text)
        html = USERNAME_REGEX.sub(self._parse_users, html)
        html = LIST_REGEX.sub(self._parse_lists, html)
        html = HASHTAG_REGEX.sub(self._parse_tags, html)
        
        # Reply?
        reply = REPLY_REGEX.match(text)
        self._reply = reply.groups(0)[0] if reply is not None else None        
        return ParseResult(self._urls, self._users, self._reply,
                           self._lists, self._tags, html)
    
    
    # Internal parser stuff ----------------------------------------------------
    def _parse_urls(self, match):
        """Parse URLs."""
        
        mat = match.group(0)
        
        # Fix a bug in the regex concerning www...com and www.-foo.com domains
        # TODO fix this in the regex instead of working around it here
        if match.group(5)[0] in '.-':
            return mat
        
        # Check for urls without http(s)
        pos = mat.find('http')
        if pos != -1:
            pre, url = mat[:pos], mat[pos:]
            full_url = url
        
        # Find the www and force http://
        else:
            pos = mat.lower().find('www')
            pre, url = mat[:pos], mat[pos:]
            full_url = 'http://%s' % url
        
        self._urls.append(url)
        return '%s%s' % (pre, self.format_url(full_url,
                                              self._shorten_url(escape(url))))
    
    def _parse_users(self, match):
        """Parse usernames."""
        
        # Don't parse lists here
        if match.group(2) is not None:
            return match.group(0)
        
        mat = match.group(0)
        self._users.append(mat[1:])
        return self.format_username(mat[0:1], mat[1:])
    
    def _parse_lists(self, match):
        """Parse lists."""
        
        # Don't parse lists here
        if match.group(4) is None:
            return match.group(0)
        
        pre, at_char, user, list_name = match.groups()
        list_name = list_name[1:]
        self._lists.append((user, list_name))
        return '%s%s' % (pre, self.format_list(at_char, user, list_name))
    
    def _parse_tags(self, match):
        """Parse hashtags."""
        
        mat = match.group(0)
        
        # Fix problems with the regex capturing stuff infront of the #
        tag = None
        for i in u'#\uff03':
            pos = mat.rfind(i)
            if pos != -1:
                tag = i
                break
        
        pre, text = mat[:pos], mat[pos + 1:]
        self._tags.append(text)
        return '%s%s' % (pre, self.format_tag(tag, text))
    
    def _shorten_url(self, text):
        """Shorten a URL and make sure to not cut of html entities."""
        
        if len(text) > self._max_url_length:
            text = text[0:self._max_url_length - 3]
            amp = text.rfind('&')
            close = text.rfind(';')
            if amp != -1 and (close == -1 or close < amp):
                text = text[0:amp]
            
            return text + '...'
        
        else:
            return text
    
    
    # User defined formatters --------------------------------------------------
    def format_tag(self, tag, text):
        """Return formatted HTML for a hashtag."""
        return '<a href="http://search.twitter.com/search?q=%s">%s%s</a>' \
                % (urllib.quote('#' + text.encode('utf-8')), tag, text)
    
    def format_username(self, at_char, user):
        """Return formatted HTML for a username."""
        return '<a href="http://twitter.com/%s">%s%s</a>' \
               % (user, at_char, user)
    
    def format_list(self, at_char, user, list_name):
        """Return formatted HTML for a list."""
        return '<a href="http://twitter.com/%s/%s">%s%s/%s</a>' \
               % (user, list_name, at_char, user, list_name)
    
    def format_url(self, url, text):
        """Return formatted HTML for a url."""
        return '<a href="%s">%s</a>' % (escape(url), text)


# Simple URL escaper
def escape(text):
    return ''.join({'&': '&amp;', '"': '&quot;',
                    '\'': '&apos;', '>': '&gt;',
                    '<': '&lt;'}.get(c, c) for c in text)

