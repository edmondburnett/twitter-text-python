# -*- coding: UTF-8 -*-
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


# Unittests --------------------------------------------------------------------
# ------------------------------------------------------------------------------

# These where taken and converted from:
# http://github.com/mzsanford/twitter-text-conformance/blob/master/autolink.yml
TESTS = {
    'username_trailing': {
        'input': u'text @username',
        'result': u'text <a href="http://twitter.com/username">@username</a>',
        'users' : [u'username']
    },
    
    'username_beginning': {
        'input': u'@username text',
        'result': u'<a href="http://twitter.com/username">@username</a> text',
        'users' : [u'username']
    },
    
    'not_username_spaced': {
        'input': u'@ username',
        'result': u'@ username',
        'users' : []
    },
    
    'not_username_preceded_letter': {
        'input': u'meet@the beach',
        'result': u'meet@the beach',
        'users' : []
    },
    
    'username_preceded_punctuation': {
        'input': u'.@username',
        'result': u'.<a href="http://twitter.com/username">@username</a>',
        'users' : [u'username']
    },
    
    'username_followed_punctuation': {
        'input': u'@username&^$%^',
        'result': u'<a href="http://twitter.com/username">@username</a>&^$%^',
        'users' : [u'username']
    }, 
    
    'username_preceded_japanese': {
        'input': u'あ@username',
        'result': u'あ<a href="http://twitter.com/username">@username</a>',
        'users' : [u'username']
    },
    
    'username_followed_japanese': {
        'input': u'@usernameの',
        'result': u'<a href="http://twitter.com/username">@username</a>の',
        'users' : [u'username']
    },
    
    'username_surrounded_japanese': {
        'input': u'あ@usernameの',
        'result': u'あ<a href="http://twitter.com/username">@username</a>の',
        'users' : [u'username']
    },
    
    'username_full_at_sign': {
        'input': u'＠username',
        'result': u'<a href="http://twitter.com/username">＠username</a>',
        'users' : [u'username']
    },
    
    'username_to_long': {
        'input': u'@username9012345678901',
        'result': u'<a href="http://twitter.com/username901234567890">@username901234567890</a>1',
        'users' : [u'username901234567890']
    }, 
    
    
    # Hashtags
    'hashtag_trailing': {
        'input': u'text #hashtag',
        'result': u'text <a href="http://search.twitter.com/search?q=%23hashtag">#hashtag</a>',
        'tags' : [u'hashtag']
    },
    
    'hashtag_alpha': {
        'input': u'text #hash0tag',
        'result': u'text <a href="http://search.twitter.com/search?q=%23hash0tag">#hash0tag</a>',
        'tags' : [u'hash0tag']
    },
      
    'hashtag_number': {
        'input': u'text #1tag',
        'result': u'text <a href="http://search.twitter.com/search?q=%231tag">#1tag</a>',
        'tags' : [u'1tag']
    },
    
    'hashtag_under': {
        'input': u'text #hash_tag',
        'result': u'text <a href="http://search.twitter.com/search?q=%23hash_tag">#hash_tag</a>',
        'tags' : [u'hash_tag']
    },
    
    'not_hashtag_number': {
        'input': u'text #1234',
        'result': u'text #1234',
        'tags' : []
    },
    
    'not_hashtag_text': {
        'input': u'text#hashtag',
        'result': u'text#hashtag',
        'tags' : []
    },
        
    'hashtag_multiple': {
        'input': u'text #hashtag1 #hashtag2',
        'result': u'text <a href="http://search.twitter.com/search?q=%23hashtag1">#hashtag1</a> <a href="http://search.twitter.com/search?q=%23hashtag2">#hashtag2</a>',
        'tags' : [u'hashtag1', u'hashtag2']
    },
            
    'hashtag_period': {
        'input': u'text.#hashtag',
        'result': u'text.<a href="http://search.twitter.com/search?q=%23hashtag">#hashtag</a>',
        'tags' : [u'hashtag']
    },
    
    'not_hashtag_escape': {
        'input': u'&#nbsp;',
        'result': u'&#nbsp;',
        'tags' : []
    },
    
    'not_hashtag_!': {
        'input': u'text #hashtag!',
        'result': u'text <a href="http://search.twitter.com/search?q=%23hashtag">#hashtag</a>!',
        'tags' : [u'hashtag']
    },
    
    
    'hashtag_japanese': {
        'input': u'text #hashtagの',
        'result': u'text <a href="http://search.twitter.com/search?q=%23hashtag">#hashtag</a>の',
        'tags' : [u'hashtag']
    },
      
    'hashtag_preceeded_full_whitespace': {
        'input': u'text　#hashtag',
        'result': u'text　<a href="http://search.twitter.com/search?q=%23hashtag">#hashtag</a>',
        'tags' : [u'hashtag']
    },
      
    'hashtag_followed_full_whitespace': {
        'input': u'#hashtag　text',
        'result': u'<a href="http://search.twitter.com/search?q=%23hashtag">#hashtag</a>　text',
        'tags' : [u'hashtag']
    },
      
    'hashtag_followed_full_hash': {
        'input': u'＃hashtag',
        'result': u'<a href="http://search.twitter.com/search?q=%23hashtag">＃hashtag</a>',
        'tags' : [u'hashtag']
    },  
      
      
    # URLS
    'url_trailing': {
        'input': u'text http://example.com',
        'result': u'text <a href="http://example.com">http://example.com</a>',
        'urls' : [u'http://example.com']
    },
    
    'url_mid': {
        'input': u'text http://example.com more text',
        'result': u'text <a href="http://example.com">http://example.com</a> more text',
        'urls' : [u'http://example.com']
    },
    
    'url_japanese': {
        'input': u'いまなにしてるhttp://example.comいまなにしてる',
        'result': u'いまなにしてる<a href="http://example.com">http://example.com</a>いまなにしてる',
        'urls' : [u'http://example.com']
    },
    
    'url_parentheses': {
        'input': u'text (http://example.com)',
        'result': u'text (<a href="http://example.com">http://example.com</a>)',
        'urls' : [u'http://example.com']
    },
    
    'url_unicode': {
        'input': u'I enjoy Macintosh Brand computers: http://✪df.ws/ejp',
        'result': u'I enjoy Macintosh Brand computers: <a href="http://✪df.ws/ejp">http://✪df.ws/ejp</a>',
        'urls' : [u'http://✪df.ws/ejp']
    },
    
    'not_url_!_domain': {
        'input': u'badly formatted http://foo!bar.com',
        'result': u'badly formatted http://foo!bar.com',
        'urls' : []
    },
    
    'not_url_under_domain': {
        'input': u'badly formatted http://foo_bar.com',
        'result': u'badly formatted http://foo_bar.com',
        'urls' : []
    },
    
    'url_preceeded_:': {
        'input': u'text:http://example.com',
        'result': u'text:<a href="http://example.com">http://example.com</a>',
        'urls' : [u'http://example.com']
    },
    

    'url_followed_?': {
        'input': u'text http://example.com?',
        'result': u'text <a href="http://example.com">http://example.com</a>?',
        'urls' : [u'http://example.com']
    },
    

    'url_followed_!': {
        'input': u'text http://example.com!',
        'result': u'text <a href="http://example.com">http://example.com</a>!',
        'urls' : [u'http://example.com']
    },
    
    'url_followed_.': {
        'input': u'text http://example.com.',
        'result': u'text <a href="http://example.com">http://example.com</a>.',
        'urls' : [u'http://example.com']
    },
    
    'url_followed_,': {
        'input': u'text http://example.com,',
        'result': u'text <a href="http://example.com">http://example.com</a>,',
        'urls' : [u'http://example.com']
    },
    
    'url_followed_:': {
        'input': u'text http://example.com:',
        'result': u'text <a href="http://example.com">http://example.com</a>:',
        'urls' : [u'http://example.com']
    },
    
    'url_followed_;': {
        'input': u'text http://example.com;',
        'result': u'text <a href="http://example.com">http://example.com</a>;',
        'urls' : [u'http://example.com']
    },
    
    'url_followed_]': {
        'input': u'text http://example.com]',
        'result': u'text <a href="http://example.com">http://example.com</a>]',
        'urls' : [u'http://example.com']
    },
    
    
    'url_followed_)': {
        'input': u'text http://example.com)',
        'result': u'text <a href="http://example.com">http://example.com</a>)',
        'urls' : [u'http://example.com']
    },
    
    'url_followed_}': {
        'input': u'text http://example.com}',
        'result': u'text <a href="http://example.com">http://example.com</a>}',
        'urls' : [u'http://example.com']
    },
    
    'url_followed_=': {
        'input': u'text http://example.com=',
        'result': u'text <a href="http://example.com">http://example.com</a>=',
        'urls' : [u'http://example.com']
    },
    
    'url_followed_\'': {
        'input': u'text http://example.com\'',
        'result': u'text <a href="http://example.com">http://example.com</a>\'',
        'urls' : [u'http://example.com']
    },
    
    'not_url_preceeded_/': {
        'input': u'text /http://example.com',
        'result': u'text /http://example.com',
        'urls' : []
    },
    
    'not_url_preceeded_!': {
        'input': u'text !http://example.com',
        'result': u'text !http://example.com',
        'urls' : []
    },
    
    'not_url_preceeded_=': {
        'input': u'text =http://example.com',
        'result': u'text =http://example.com',
        'urls' : []
    },
    
    'url_embed_link': {
        'input': u'<link rel=\'true\'>http://example.com</link>',
        'result': u'<link rel=\'true\'><a href="http://example.com">http://example.com</a></link>',
        'urls' : [u'http://example.com']
    },
    
    'url_multiple': {
        'input': u'http://example.com https://sslexample.com http://sub.example.com',
        'result': u'<a href="http://example.com">http://example.com</a> <a href="https://sslexample.com">https://sslexample.com</a> <a href="http://sub.example.com">http://sub.example.com</a>',
        'urls' : [u'http://example.com', u'https://sslexample.com', u'http://sub.example.com']
    },
    
    'url_long_tld': {
        'input': u'http://example.mobi/path',
        'result': u'<a href="http://example.mobi/path">http://example.mobi/path</a>',
        'urls' : [u'http://example.mobi/path']
    },
    
    'url_www': {
        'input': u'www.example.com',
        'result': u'<a href="http://www.example.com">www.example.com</a>',
        'urls' : [u'www.example.com']
    },
    
    'url_WWW': {
        'input': u'WWW.EXAMPLE.COM',
        'result': u'<a href="http://WWW.EXAMPLE.COM">WWW.EXAMPLE.COM</a>',
        'urls' : [u'WWW.EXAMPLE.COM']
    },
     
    'url_multiple_protocols': {
        'input': u'http://foo.com AND https://bar.com AND www.foobar.com',
        'result': u'<a href="http://foo.com">http://foo.com</a> AND <a href="https://bar.com">https://bar.com</a> AND <a href="http://www.foobar.com">www.foobar.com</a>',
        'urls' : [u'http://foo.com', u'https://bar.com', u'www.foobar.com']
    },
    
    'url_raw_domain': {
        'input': u'See http://example.com example.com',
        'result': u'See <a href="http://example.com">http://example.com</a> example.com',
        'urls' : [u'http://example.com']
    },

    'url_at_numeric': {
        'input': u'http://www.flickr.com/photos/29674651@N00/4382024406',
        'result': u'<a href="http://www.flickr.com/photos/29674651@N00/4382024406">http://www.flickr.com/photo...</a>',
        'urls' : [u'http://www.flickr.com/photos/29674651@N00/4382024406']
    },
    
    'url_at_non_numeric': {
        'input': u'http://www.flickr.com/photos/29674651@N00/foobar',
        'result': u'<a href="http://www.flickr.com/photos/29674651@N00/foobar">http://www.flickr.com/photo...</a>',
        'urls' : [u'http://www.flickr.com/photos/29674651@N00/foobar']
    },  
    
    'url_only_domain_followed_period': {
        'input': u'I think it\'s proper to end sentences with a period http://tell.me. Even when they contain a URL.',
        'result': u'I think it\'s proper to end sentences with a period <a href="http://tell.me">http://tell.me</a>. Even when they contain a URL.',
        'urls' : [u'http://tell.me']
    },  
    
    'url_only_domain_path_followed_period': {
        'input': u'I think it\'s proper to end sentences with a period http://tell.me/why. Even when they contain a URL.',
        'result': u'I think it\'s proper to end sentences with a period <a href="http://tell.me/why">http://tell.me/why</a>. Even when they contain a URL.',
        'urls' : [u'http://tell.me/why']
    },  
    
    'url_only_domain_query_followed_period': {
        'input': u'I think it\'s proper to end sentences with a period http://tell.me/why?=because.i.want.it. Even when they contain a URL.',
        'result': u'I think it\'s proper to end sentences with a period <a href="http://tell.me/why?=because.i.want.it">http://tell.me/why?=because...</a>. Even when they contain a URL.',
        'urls' : [u'http://tell.me/why?=because.i.want.it']
    },  
    
    'not_url_...': {
        'input': u'Is www...foo a valid URL?',
        'result': u'Is www...foo a valid URL?',
        'urls' : []
    },
    
    'not_url_-': {
        'input': u'Is www.-foo.com a valid URL?',
        'result': u'Is www.-foo.com a valid URL?',
        'urls' : []
    },
    
    'url_-': {
        'input': u'Is www.foo-bar.com a valid URL?',
        'result': u'Is <a href="http://www.foo-bar.com">www.foo-bar.com</a> a valid URL?',
        'urls' : [u'www.foo-bar.com']
    },
    
    'url_&lang=': {
        'input': u'Check out http://search.twitter.com/search?q=avro&lang=en',
        'result': u'Check out <a href="http://search.twitter.com/search?q=avro&amp;lang=en">http://search.twitter.com/s...</a>',
        'urls' : [u'http://search.twitter.com/search?q=avro&lang=en']
    },
    
    'url_&break': {
        'input': u'Check out http://twitter.com/te?foo&invalid=True',
        'result': u'Check out <a href="http://twitter.com/te?foo&amp;invalid=True">http://twitter.com/te?foo...</a>',
        'urls' : [u'http://twitter.com/te?foo&invalid=True']
    },
    
    # ALL
    'all_not_break_url_at': {
        'input': u'http://www.flickr.com/photos/29674651@N00/4382024406',
        'result': u'<a href="http://www.flickr.com/photos/29674651@N00/4382024406">http://www.flickr.com/photo...</a>',
        'urls' : [u'http://www.flickr.com/photos/29674651@N00/4382024406']
    },  
      
    'all_not_allow_amp_without_question': {
        'input': u'Check out: http://www.github.com/test&@username',
        'result': u'Check out: <a href="http://www.github.com/test">http://www.github.com/test</a>&<a href="http://twitter.com/username">@username</a>',
        'urls' : [u'http://www.github.com/test'],
        'users' : [u'username']
    }
}


# Really bad unit tester!
if __name__ == '__main__':
    import format
    f = format.Formatter()
    PASSED = 0
    FAILED = 0
    for k in TESTS:
        test = TESTS[k]
    
        expected = test['result']
        result = f.parse(test['input'])
        
        # Users
        if test.has_key('users') and test['users'] != f.users:
            print '#%s - Failed!' % k
            print 'E USERS: %s' % test['users']
            print 'R USERS: %s' % f.users
            FAILED += 1
        
        # Tags
        elif test.has_key('tags') and test['tags'] != f.tags:
            print '#%s - Failed!' % k
            print 'E TAGS: %s' % test['tags']
            print 'R TAGS: %s' % f.tags
            FAILED += 1
        
        
        # URLS
        elif test.has_key('urls') and test['urls'] != f.urls:
            print '#%s - Failed!' % k
            print 'E URLS: %s' % test['urls']
            print 'R URLS: %s' % f.urls
            FAILED += 1
        
        # Text
        elif result == expected:
            #print '#%s - Passed' % k
            PASSED += 1
        
        else:
            FAILED += 1
            print '#%s - Failed!' % k
            print 'E: %s' % expected
            print 'R: %s' % result
    
    print "%d passed. %d failed." % (PASSED, FAILED)

