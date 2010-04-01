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

# TODO add support for lists
# TODO create a setup.py
# TODO cleanup the unittests


# Tweet Parser and Formatter ---------------------------------------------------
# ------------------------------------------------------------------------------
import re
import urllib

# Some of this code has been translated from the twitter-text-java library:
# <http://github.com/mzsanford/twitter-text-java>
USERNAME_REGEX = re.compile(ur'\B[@\uff20]([a-z0-9_]{1,20})', re.IGNORECASE)

UTF_CHARS = ur'a-z0-9_\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u00ff'
HASHTAG_EXP = ur'(^|[^0-9A-Z&/]+)(#|\uff03)([0-9A-Z_]*[A-Z_]+[%s]*)' % UTF_CHARS
HASHTAG_REGEX = re.compile(HASHTAG_EXP, re.IGNORECASE)

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
    """A class containing the results of a parsed Tweet."""
    
    def __init__(self, urls, users, tags, html):
        self.urls = urls
        self.users = users
        self.tags = tags
        self.html = html


class Parser:
    """A Tweet Parser"""
    
    def __init__(self, max_url_length=30):
        self._max_url_length = max_url_length
        self._url_parts = []
        self._parts = []
    
    def parse(self, text):
        """Parse the text and return a ParseResult instance."""
        
        # Reset
        self._urls = []
        self._users = []
        self._tags = []
        
        # Filter
        html = URL_REGEX.sub(self._parse_urls, text)
        html = USERNAME_REGEX.sub(self._parse_users, html)
        html = HASHTAG_REGEX.sub(self._parse_tags, html)
        
        return ParseResult(self._urls, self._users, self._tags, html)
    
    
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
        
        mat = match.group(0)
        self._users.append(mat[1:])
        return self.format_username(mat[0:1], mat[1:])
    
    def _parse_tags(self, match):
        """Parse hashtags."""
        
        mat = match.group(0)
        
        # Fix problems with the regex capturing stuff infront of the #
        for tag in u'#\uff03':
            pos = mat.rfind(tag)
            if pos != -1:
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
    
    def format_url(self, url, text):
        """Return formatted HTML for a url."""
        return '<a href="%s">%s</a>' % (escape(url), text)


# Simple URL escaper
def escape(text):
    return ''.join({'&': '&amp;', '"': '&quot;',
                    '\'': '&apos;', '>': '&gt;',
                    '<': '&lt;'}.get(c, c) for c in text)

