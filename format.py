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


class Formatter:
    def __init__(self):
        self.__urls = []
        self.__parts = []
        self.urls = []
        self.users = []
        self.tags = []
    
    # Parsing ------------------------------------------------------------------
    def parse(self, text):
        self.__urls = []
        self.urls = []
        self.users = []
        self.tags = []
        URL_REGEX.sub(self.url, text)
        
        # Filter URLS
        self.__parts = []
        last = 0
        for i in self.__urls:
            # Fix regex problems
            domain = i.group(5)
            if not domain[0] in '.-':
                self.__parts.append((0, text[last:i.start()]))
                self.__parts.append((1, text[i.start():i.end()]))
                last = i.end()
            
        self.__parts.append((0, text[last:]))
        self.filter_by(AT_REGEX, 2) # Filter @
        self.filter_by(TAG_REGEX, 3) # Filter Hashtags
        return self.format()
    
    def filter_by(self, regex, stype):
        pos = 0
        while pos < len(self.__parts):
            ttype, data = self.__parts[pos]
            if ttype == 0:
                match = regex.search(data)
                if match is not None:
                    self.__parts.pop(pos)
                    self.__parts.insert(pos,
                                    (0, data[:match.start()]))
                    
                    self.__parts.insert(pos + 1,
                                    (stype, data[match.start():match.end()]))
                    
                    self.__parts.insert(pos + 2,
                                    (0, data[match.end():]))
                    pos += 1
            
            pos += 1
    
    def url(self, match):
        self.__urls.append(match)
    
    
    # Formatting ---------------------------------------------------------------
    def format(self):
        result = []
        for i in self.__parts:
            ttype, data = i
            if ttype == 0:
                result.append(data)
            
            # URL
            elif ttype == 1:
                # Fix a bug in the Regex
                start = data.find('http')
                if start == -1:
                    start = data.lower().find('www')
                
                pre = ''
                if start != -1:
                    pre = data[:start]
                    data = data[start:]
                
                self.urls.append(data)
                text_data = data
                if data.lower().startswith('www'):
                    data = 'http://%s' % data
                
                result.append('%s%s' % (pre, self.format_url(data, text_data)))
            
            # username
            elif ttype == 2:
                at = data[0:1]
                user = data[1:]
                self.users.append(user)
                result.append(self.format_username(at, user))
            
            # hashtag
            elif ttype == 3:
                pos = data.rfind('#')
                tag = '#'
                if pos == -1:
                    tag = u'\uff03'
                    pos = data.rfind(tag)
                    
                pre, text = data[:pos], data[pos + 1:]
                self.tags.append(text)
                result.append('%s%s' % (pre, self.format_tag(tag, text)))
        
        return ''.join(result)
    
    def format_tag(self, tag, text):
        return '<a href="http://search.twitter.com/search?%s">%s%s</a>' \
                % (urllib.urlencode({'q': '#' + text}), tag, text)
    
    def format_username(self, at, user):
        return '<a href="http://twitter.com/%s">%s%s</a>' \
                % (user, at, user)
    
    def format_url(self, url, text):
        if len(text) > 30:
            text = text[0:27]
            amp = text.rfind('&')
            close = text.rfind(';')
            if amp != -1 and (close == -1 or close < amp):
                text = text[0:amp]
        
            text += '...'
        
        return '<a href="%s">%s</a>' \
                % (escape(url), escape(text))

