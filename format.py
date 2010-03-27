#  This file is part of AtarashiiFormat.
#
#  AtarashiiFormat is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  AtarashiiFormat is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with
#  AtarashiiFormat. If not, see <http://www.gnu.org/licenses/>.

# TODO add support for lists

# Tweet Parser and Formatter ---------------------------------------------------
# ------------------------------------------------------------------------------
import re
import urllib

ENTITIES = {
    '&': '&amp;',
    '"': '&quot;',
    '\'': '&apos;',
    '>': '&gt;',
    '<': '&lt;'
}
def escape(text):
    return ''.join(ENTITIES.get(c, c) for c in text)  

                                       
# Some of this code has been translated from the twitter-text-java library:
# <http://github.com/mzsanford/twitter-text-java>
AT_REGEX = re.compile(ur'\B[@\uff20]([a-z0-9_]{1,20})', re.IGNORECASE)

UTF_CHARS = ur'a-z0-9_\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u00ff'
TAG_EXP = ur'(^|[^0-9A-Z&/]+)(#|\uff03)([0-9A-Z_]*[A-Z_]+[%s]*)' % UTF_CHARS
TAG_REGEX = re.compile(TAG_EXP, re.IGNORECASE)

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
                       + QUERY_ENDING_CHARS + ')?))', re.UNICODE |re.IGNORECASE)


# Part constants
PART_TEXT = 0
PART_URL = 1
PART_USER = 2
PART_TAG = 3


class Formatter:
    def __init__(self, max_url_length=30):
        self.__max_url_length = max_url_length
        self.__urls = []
        self.__parts = []
        
        self.urls = []
        self.users = []
        self.tags = []
    
    # Parsing ------------------------------------------------------------------
    def parse(self, text):
        # Reset
        self.urls = []
        self.users = []
        self.tags = []
        
        # Filter URLS first to make sure we get no problems with # and @ in them
        self.__urls = []
        URL_REGEX.sub(self.url, text)
        self.__parts = []
        last = 0
        for i in self.__urls:
            # Fix regex problems with wrongly formatted domains 
            # e.g. www...foo www.-foo
            if not i.group(5)[0] in '.-':
                self.__parts.append((PART_TEXT, text[last:i.start()]))
                self.__parts.append((PART_URL, text[i.start():i.end()]))
                last = i.end()
            
        self.__parts.append((PART_TEXT, text[last:]))
        
        # Filter usernames
        self.filter_by(AT_REGEX, PART_USER)
        
        # Filter hashtags
        self.filter_by(TAG_REGEX, PART_TAG)
        return self.format()
    
    def filter_by(self, regex, filter_type):
        pos = 0
        while pos < len(self.__parts):
            cur_type, data = self.__parts[pos]
            if cur_type == PART_TEXT:
                match = regex.search(data)
                if match is not None:
                    self.__parts.pop(pos)
                    self.__parts.insert(pos, (PART_TEXT, data[:match.start()]))
                    self.__parts.insert(pos + 1,
                                       (filter_type,
                                        data[match.start():match.end()]))
                    
                    self.__parts.insert(pos + 2, (PART_TEXT,
                                                  data[match.end():]))
                    
                    pos += 1
            
            pos += 1
    
    def url(self, match):
        self.__urls.append(match)
    
    
    # Formatting ---------------------------------------------------------------
    def format(self):
        result = []
        for i in self.__parts:
            part_type, data = i
            
            # Plain text
            if part_type == PART_TEXT:
                result.append(data)
            
            # URLs
            elif part_type == PART_URL:
                # Check for urls without http(s)
                start = data.find('http')
                if start == -1:
                    # Find the www
                    start = data.lower().find('www')
                    pre, data = data[:start], data[start:]
                    
                    # Force at least http://
                    url = 'http://%s' % data
                
                else:
                    pre, url = data[:start], data[start:]
                    data = url
                
                self.urls.append(data)
                result.append('%s%s' % (pre, self.format_url(url, data)))
            
            # Usernames
            elif part_type == PART_USER:
                at = data[0:1]
                user = data[1:]
                self.users.append(user)
                result.append(self.format_username(at, user))
            
            # Hashtags 
            elif part_type == PART_TAG:
                # Fix problems with the regex capturing stuff infront of the #
                for i in u'#\uff03':
                    tag = i
                    pos = data.rfind(tag)
                    if pos != -1:
                        break
                
                pre, text = data[:pos], data[pos + 1:]
                self.tags.append(text)
                result.append('%s%s' % (pre, self.format_tag(tag, text)))
        
        return ''.join(result)
    
    def format_tag(self, tag, text):
        return '<a href="http://search.twitter.com/search?%s">%s%s</a>' \
                % (urllib.urlencode({'q': '#' + text}), tag, text)
    
    def format_username(self, at, user):
        return '<a href="http://twitter.com/%s">%s%s</a>' % (user, at, user)
    
    def format_url(self, url, text):
        # Shorten the URL text and make sure we don't cut of html entities
        if len(text) > self.__max_url_length:
            text = text[0:self.__max_url_length - 3]
            amp = text.rfind('&')
            close = text.rfind(';')
            if amp != -1 and (close == -1 or close < amp):
                text = text[0:amp]
            
            text += '...'
        
        return '<a href="%s">%s</a>' % (escape(url), escape(text))

