# -*- coding: UTF-8 -*-
#  This file is part of twitter-text-python.
#
#  twitter-text-python is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  twitter-text-python is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with
#  twitter-text-python. If not, see <http://www.gnu.org/licenses/>.


# twp - Unittests --------------------------------------------------------------
# ------------------------------------------------------------------------------
import unittest
import ttp


class TWPTests(unittest.TestCase):

    def setUp(self):
        self.parser = ttp.Parser()

    # General Tests ------------------------------------------------------------
    # --------------------------------------------------------------------------
    def test_urls(self):
        """Confirm that # in a URL works along with ,"""
        result = self.parser.parse(u'big url: http://blah.com:8080/path/to/here?p=1&q=abc,def#posn2 #ahashtag')
        self.assertEqual(result.urls, [u'http://blah.com:8080/path/to/here?p=1&q=abc,def#posn2'])
        self.assertEqual(result.tags, [u'ahashtag'])

    def test_all_not_allow_amp_without_question(self):
        result = self.parser.parse(u'Check out: http://www.github.com/test&@username')
        self.assertEqual(result.html, u'Check out: <a href="http://www.github.com/test">http://www.github.com/test</a>&<a href="http://twitter.com/username">@username</a>')
        self.assertEqual(result.users, [u'username'])
        self.assertEqual(result.urls, [u'http://www.github.com/test'])

    def test_all_not_break_url_at(self):
        result = self.parser.parse(u'http://www.flickr.com/photos/29674651@N00/4382024406')
        self.assertEqual(result.html, u'<a href="http://www.flickr.com/photos/29674651@N00/4382024406">http://www.flickr.com/photo...</a>')
        self.assertEqual(result.urls, [u'http://www.flickr.com/photos/29674651@N00/4382024406'])

    # URL tests ----------------------------------------------------------------
    # --------------------------------------------------------------------------
    def test_url_mid(self):
        result = self.parser.parse(u'text http://example.com more text')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a> more text')
        self.assertEqual(result.urls, [u'http://example.com'])

    def test_url_unicode(self):
        result = self.parser.parse(u'I enjoy Macintosh Brand computers: http://✪df.ws/ejp')
        self.assertEqual(result.html, u'I enjoy Macintosh Brand computers: <a href="http://✪df.ws/ejp">http://✪df.ws/ejp</a>')
        self.assertEqual(result.urls, [u'http://\u272adf.ws/ejp'])

    def test_url_parentheses(self):
        result = self.parser.parse(u'text (http://example.com)')
        self.assertEqual(result.html, u'text (<a href="http://example.com">http://example.com</a>)')
        self.assertEqual(result.urls, [u'http://example.com'])

    def test_url_underscore(self):
        result = self.parser.parse(u'text http://example.com/test/foo_123.jpg')
        self.assertEqual(result.html, u'text <a href="http://example.com/test/foo_123.jpg">http://example.com/test/foo...</a>')
        self.assertEqual(result.urls, [u'http://example.com/test/foo_123.jpg'])

    def test_url_underscore_dot(self):
        result = self.parser.parse(u'text http://example.com/test/bla.net_foo_123.jpg')
        self.assertEqual(result.html, u'text <a href="http://example.com/test/bla.net_foo_123.jpg">http://example.com/test/bla...</a>')
        self.assertEqual(result.urls, [u'http://example.com/test/bla.net_foo_123.jpg'])

    def test_url_amp_lang_equals(self):
        result = self.parser.parse(u'Check out http://twitter.com/search?q=avro&lang=en')
        self.assertEqual(result.html, u'Check out <a href="http://twitter.com/search?q=avro&amp;lang=en">http://twitter.com/s...</a>')
        self.assertEqual(result.urls, [u'http://twitter.com/search?q=avro&lang=en'])

    def test_url_amp_break(self):
        result = self.parser.parse(u'Check out http://twitter.com/te?foo&invalid=True')
        self.assertEqual(result.html, u'Check out <a href="http://twitter.com/te?foo&amp;invalid=True">http://twitter.com/te?foo...</a>')
        self.assertEqual(result.urls, [u'http://twitter.com/te?foo&invalid=True'])

    def test_url_dash(self):
        result = self.parser.parse(u'Is www.foo-bar.com a valid URL?')
        self.assertEqual(result.html, u'Is <a href="http://www.foo-bar.com">www.foo-bar.com</a> a valid URL?')
        self.assertEqual(result.urls, [u'www.foo-bar.com'])

    def test_url_multiple(self):
        result = self.parser.parse(u'http://example.com https://sslexample.com http://sub.example.com')
        self.assertEqual(
            result.html, u'<a href="http://example.com">http://example.com</a> <a href="https://sslexample.com">https://sslexample.com</a> <a href="http://sub.example.com">http://sub.example.com</a>')
        self.assertEqual(result.urls, [u'http://example.com', u'https://sslexample.com', u'http://sub.example.com'])

    def test_url_raw_domain(self):
        result = self.parser.parse(u'See http://example.com example.com')
        self.assertEqual(result.html, u'See <a href="http://example.com">http://example.com</a> example.com')
        self.assertEqual(result.urls, [u'http://example.com'])

    def test_url_embed_link(self):
        result = self.parser.parse(u'<link rel=\'true\'>http://example.com</link>')
        self.assertEqual(result.html, u'<link rel=\'true\'><a href="http://example.com">http://example.com</a></link>')
        self.assertEqual(result.urls, [u'http://example.com'])

    def test_url_trailing(self):
        result = self.parser.parse(u'text http://example.com')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>')
        self.assertEqual(result.urls, [u'http://example.com'])

    def test_url_japanese(self):
        result = self.parser.parse(u'いまなにしてるhttp://example.comいまなにしてる')
        self.assertEqual(result.html, u'いまなにしてる<a href="http://example.com">http://example.com</a>いまなにしてる')
        self.assertEqual(result.urls, [u'http://example.com'])

    def test_url_lots_of_punctuation(self):
        result = self.parser.parse(u'text http://xo.com/~matthew+%-,.;x')
        self.assertEqual(result.html, u'text <a href="http://xo.com/~matthew+%-,.;x">http://xo.com/~matthew+%-,.;x</a>')
        self.assertEqual(result.urls, [u'http://xo.com/~matthew+%-,.;x'])

    def test_url_question_numbers(self):
        result = self.parser.parse(u'text http://example.com/?77e8fd')
        self.assertEqual(result.html, u'text <a href="http://example.com/?77e8fd">http://example.com/?77e8fd</a>')
        self.assertEqual(result.urls, [u'http://example.com/?77e8fd'])

    def test_url_one_letter_other(self):
        result = self.parser.parse(u'text http://u.nu/')
        self.assertEqual(result.html, u'text <a href="http://u.nu/">http://u.nu/</a>')
        self.assertEqual(result.urls, [u'http://u.nu/'])

        result = self.parser.parse(u'text http://u.tv/')
        self.assertEqual(result.html, u'text <a href="http://u.tv/">http://u.tv/</a>')
        self.assertEqual(result.urls, [u'http://u.tv/'])

    def test_url_one_letter_iana(self):
        result = self.parser.parse(u'text http://x.com/')
        self.assertEqual(result.html, u'text <a href="http://x.com/">http://x.com/</a>')
        self.assertEqual(result.urls, [u'http://x.com/'])

        result = self.parser.parse(u'text http://Q.com/')
        self.assertEqual(result.html, u'text <a href="http://Q.com/">http://Q.com/</a>')
        self.assertEqual(result.urls, [u'http://Q.com/'])

        result = self.parser.parse(u'text http://z.com/')
        self.assertEqual(result.html, u'text <a href="http://z.com/">http://z.com/</a>')
        self.assertEqual(result.urls, [u'http://z.com/'])

        result = self.parser.parse(u'text http://i.net/')
        self.assertEqual(result.html, u'text <a href="http://i.net/">http://i.net/</a>')
        self.assertEqual(result.urls, [u'http://i.net/'])

        result = self.parser.parse(u'text http://q.net/')
        self.assertEqual(result.html, u'text <a href="http://q.net/">http://q.net/</a>')
        self.assertEqual(result.urls, [u'http://q.net/'])

        result = self.parser.parse(u'text http://X.org/')
        self.assertEqual(result.html, u'text <a href="http://X.org/">http://X.org/</a>')
        self.assertEqual(result.urls, [u'http://X.org/'])

    def test_url_long_hypens(self):
        result = self.parser.parse(u'text http://word-and-a-number-8-ftw.domain.tld/')
        self.assertEqual(result.html, u'text <a href="http://word-and-a-number-8-ftw.domain.tld/">http://word-and-a-number-8-...</a>')
        self.assertEqual(result.urls, [u'http://word-and-a-number-8-ftw.domain.tld/'])

    # URL not tests ------------------------------------------------------------
    def test_not_url_dotdotdot(self):
        result = self.parser.parse(u'Is www...foo a valid URL?')
        self.assertEqual(result.html, u'Is www...foo a valid URL?')
        self.assertEqual(result.urls, [])

    def test_not_url_dash(self):
        result = self.parser.parse(u'Is www.-foo.com a valid URL?')
        self.assertEqual(result.html, u'Is www.-foo.com a valid URL?')
        self.assertEqual(result.urls, [])

    def test_not_url_no_tld(self):
        result = self.parser.parse(u'Is http://no-tld a valid URL?')
        self.assertEqual(result.html, u'Is http://no-tld a valid URL?')
        self.assertEqual(result.urls, [])

    def test_not_url_tld_too_short(self):
        result = self.parser.parse(u'Is http://tld-too-short.x a valid URL?')
        self.assertEqual(result.html, u'Is http://tld-too-short.x a valid URL?')
        self.assertEqual(result.urls, [])

    def test_all_not_break_url_at2(self):
        result = self.parser.parse(u'http://www.flickr.com/photos/29674651@N00/4382024406')
        self.assertEqual(result.html, u'<a href="http://www.flickr.com/photos/29674651@N00/4382024406">http://www.flickr.com/photo...</a>')
        self.assertEqual(result.urls, [u'http://www.flickr.com/photos/29674651@N00/4382024406'])

    def test_not_url_one_letter_iana(self):
        result = self.parser.parse(u'text http://a.com/ http://a.net/ http://a.org/')
        self.assertEqual(result.html, u'text http://a.com/ http://a.net/ http://a.org/')
        self.assertEqual(result.urls, [])

    # URL followed Tests -------------------------------------------------------
    def test_url_followed_question(self):
        result = self.parser.parse(u'text http://example.com?')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>?')
        self.assertEqual(result.urls, [u'http://example.com'])

    def test_url_followed_colon(self):
        result = self.parser.parse(u'text http://example.com:')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>:')
        self.assertEqual(result.urls, [u'http://example.com'])

    def test_url_followed_curly_brace(self):
        result = self.parser.parse(u'text http://example.com}')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>}')
        self.assertEqual(result.urls, [u'http://example.com'])

    def test_url_followed_single_quote(self):
        result = self.parser.parse(u'text http://example.com')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>')
        self.assertEqual(result.urls, [u'http://example.com'])

    def test_url_followed_dot(self):
        result = self.parser.parse(u'text http://example.com.')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>.')
        self.assertEqual(result.urls, [u'http://example.com'])

    def test_url_followed_exclamation(self):
        result = self.parser.parse(u'text http://example.com!')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>!')
        self.assertEqual(result.urls, [u'http://example.com'])

    def test_url_followed_comma(self):
        result = self.parser.parse(u'text http://example.com,')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>,')
        self.assertEqual(result.urls, [u'http://example.com'])

    def test_url_with_path_preceeded_by_comma(self):
        result = self.parser.parse(u'text ,http://example.com/abcde, more')
        self.assertEqual(result.html, u'text ,<a href="http://example.com/abcde">http://example.com/abcde</a>, more')
        self.assertEqual(result.urls, [u'http://example.com/abcde'])

    def test_url_with_path_followed_comma(self):
        result = self.parser.parse(u'text http://example.com/abcde, more')
        self.assertEqual(result.html, u'text <a href="http://example.com/abcde">http://example.com/abcde</a>, more')
        self.assertEqual(result.urls, [u'http://example.com/abcde'])

    def test_url_with_path_followed_commas(self):
        result = self.parser.parse(u'text http://example.com/abcde,, more')
        self.assertEqual(result.html, u'text <a href="http://example.com/abcde">http://example.com/abcde</a>,, more')
        self.assertEqual(result.urls, [u'http://example.com/abcde'])

    def test_url_followed_brace(self):
        result = self.parser.parse(u'text http://example.com)')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>)')
        self.assertEqual(result.urls, [u'http://example.com'])

    def test_url_followed_big_brace(self):
        result = self.parser.parse(u'text http://example.com]')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>]')
        self.assertEqual(result.urls, [u'http://example.com'])

    def test_url_followed_equals(self):
        result = self.parser.parse(u'text http://example.com=')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>=')
        self.assertEqual(result.urls, [u'http://example.com'])

    def test_url_followed_semicolon(self):
        result = self.parser.parse(u'text http://example.com;')
        self.assertEqual(result.html, u'text <a href="http://example.com">http://example.com</a>;')
        self.assertEqual(result.urls, [u'http://example.com'])

    def test_url_followed_hypen(self):
        result = self.parser.parse(u'text http://domain.tld-that-you-should-have-put-a-space-after')
        self.assertEqual(result.html, u'text <a href="http://domain.tld">http://domain.tld</a>-that-you-should-have-put-a-space-after')
        self.assertEqual(result.urls, [u'http://domain.tld'])

    # URL preceeded Tests -------------------------------------------------------
    def test_url_preceeded_colon(self):
        result = self.parser.parse(u'text:http://example.com')
        self.assertEqual(result.html, u'text:<a href="http://example.com">http://example.com</a>')
        self.assertEqual(result.urls, [u'http://example.com'])

    def test_not_url_preceeded_equals(self):
        result = self.parser.parse(u'text =http://example.com')
        self.assertEqual(result.html, u'text =http://example.com')
        self.assertEqual(result.urls, [])

    # NOT
    def test_not_url_preceeded_forwardslash(self):
        result = self.parser.parse(u'text /http://example.com')
        self.assertEqual(result.html, u'text /http://example.com')
        self.assertEqual(result.urls, [])

    def test_not_url_preceeded_exclamation(self):
        result = self.parser.parse(u'text !http://example.com')
        self.assertEqual(result.html, u'text !http://example.com')
        self.assertEqual(result.urls, [])

    # URL numeric tests --------------------------------------------------------
    def test_url_at_numeric(self):
        result = self.parser.parse(u'http://www.flickr.com/photos/29674651@N00/4382024406')
        self.assertEqual(result.html, u'<a href="http://www.flickr.com/photos/29674651@N00/4382024406">http://www.flickr.com/photo...</a>')
        self.assertEqual(result.urls, [u'http://www.flickr.com/photos/29674651@N00/4382024406'])

    def test_url_at_non_numeric(self):
        result = self.parser.parse(u'http://www.flickr.com/photos/29674651@N00/foobar')
        self.assertEqual(result.html, u'<a href="http://www.flickr.com/photos/29674651@N00/foobar">http://www.flickr.com/photo...</a>')
        self.assertEqual(result.urls, [u'http://www.flickr.com/photos/29674651@N00/foobar'])

    # URL domain tests ---------------------------------------------------------
    def test_url_WWW(self):
        result = self.parser.parse(u'WWW.EXAMPLE.COM')
        self.assertEqual(result.html, u'<a href="http://WWW.EXAMPLE.COM">WWW.EXAMPLE.COM</a>')
        self.assertEqual(result.urls, [u'WWW.EXAMPLE.COM'])

    def test_url_www(self):
        result = self.parser.parse(u'www.example.com')
        self.assertEqual(result.html, u'<a href="http://www.example.com">www.example.com</a>')
        self.assertEqual(result.urls, [u'www.example.com'])

    def test_url_only_domain_query_followed_period(self):
        result = self.parser.parse(u'I think it\'s proper to end sentences with a period http://tell.me/why?=because.i.want.it. Even when they contain a URL.')
        self.assertEqual(
            result.html, u'I think it\'s proper to end sentences with a period <a href="http://tell.me/why?=because.i.want.it">http://tell.me/why?=because...</a>. Even when they contain a URL.')
        self.assertEqual(result.urls, [u'http://tell.me/why?=because.i.want.it'])

    def test_url_only_domain_followed_period(self):
        result = self.parser.parse(u'I think it\'s proper to end sentences with a period http://tell.me. Even when they contain a URL.')
        self.assertEqual(result.html, u'I think it\'s proper to end sentences with a period <a href="http://tell.me">http://tell.me</a>. Even when they contain a URL.')
        self.assertEqual(result.urls, [u'http://tell.me'])

    def test_url_only_domain_path_followed_period(self):
        result = self.parser.parse(u'I think it\'s proper to end sentences with a period http://tell.me/why. Even when they contain a URL.')
        self.assertEqual(result.html, u'I think it\'s proper to end sentences with a period <a href="http://tell.me/why">http://tell.me/why</a>. Even when they contain a URL.')
        self.assertEqual(result.urls, [u'http://tell.me/why'])

    def test_url_long_tld(self):
        result = self.parser.parse(u'http://example.mobi/path')
        self.assertEqual(result.html, u'<a href="http://example.mobi/path">http://example.mobi/path</a>')
        self.assertEqual(result.urls, [u'http://example.mobi/path'])

    def test_url_multiple_protocols(self):
        result = self.parser.parse(u'http://foo.com AND https://bar.com AND www.foobar.com')
        self.assertEqual(result.html, u'<a href="http://foo.com">http://foo.com</a> AND <a href="https://bar.com">https://bar.com</a> AND <a href="http://www.foobar.com">www.foobar.com</a>')
        self.assertEqual(result.urls, [u'http://foo.com', u'https://bar.com', u'www.foobar.com'])

    # NOT
    def test_not_url_exclamation_domain(self):
        result = self.parser.parse(u'badly formatted http://foo!bar.com')
        self.assertEqual(result.html, u'badly formatted http://foo!bar.com')
        self.assertEqual(result.urls, [])

    def test_not_url_under_domain(self):
        result = self.parser.parse(u'badly formatted http://foo_bar.com')
        self.assertEqual(result.html, u'badly formatted http://foo_bar.com')
        self.assertEqual(result.urls, [])

    # Hashtag tests ------------------------------------------------------------
    # --------------------------------------------------------------------------
    def test_hashtag_followed_full_whitespace(self):
        result = self.parser.parse(u'#hashtag　text')
        self.assertEqual(result.html, u'<a href="http://search.twitter.com/search?q=%23hashtag">#hashtag</a>　text')
        self.assertEqual(result.tags, [u'hashtag'])

    def test_hashtag_followed_full_hash(self):
        result = self.parser.parse(u'＃hashtag')
        self.assertEqual(result.html, u'<a href="http://search.twitter.com/search?q=%23hashtag">＃hashtag</a>')
        self.assertEqual(result.tags, [u'hashtag'])

    def test_hashtag_preceeded_full_whitespace(self):
        result = self.parser.parse(u'text　#hashtag')
        self.assertEqual(result.html, u'text　<a href="http://search.twitter.com/search?q=%23hashtag">#hashtag</a>')
        self.assertEqual(result.tags, [u'hashtag'])

    def test_hashtag_number(self):
        result = self.parser.parse(u'text #1tag')
        self.assertEqual(result.html, u'text <a href="http://search.twitter.com/search?q=%231tag">#1tag</a>')
        self.assertEqual(result.tags, [u'1tag'])

    def test_not_hashtag_escape(self):
        result = self.parser.parse(u'&#nbsp;')
        self.assertEqual(result.html, u'&#nbsp;')
        self.assertEqual(result.tags, [])

    def test_hashtag_japanese(self):
        result = self.parser.parse(u'text #hashtagの')
        self.assertEqual(result.html, u'text <a href="http://search.twitter.com/search?q=%23hashtag">#hashtag</a>の')
        self.assertEqual(result.tags, [u'hashtag'])

    def test_hashtag_period(self):
        result = self.parser.parse(u'text.#hashtag')
        self.assertEqual(result.html, u'text.<a href="http://search.twitter.com/search?q=%23hashtag">#hashtag</a>')
        self.assertEqual(result.tags, [u'hashtag'])

    def test_hashtag_trailing(self):
        result = self.parser.parse(u'text #hashtag')
        self.assertEqual(result.html, u'text <a href="http://search.twitter.com/search?q=%23hashtag">#hashtag</a>')
        self.assertEqual(result.tags, [u'hashtag'])

    def test_not_hashtag_exclamation(self):
        result = self.parser.parse(u'text #hashtag!')
        self.assertEqual(result.html, u'text <a href="http://search.twitter.com/search?q=%23hashtag">#hashtag</a>!')
        self.assertEqual(result.tags, [u'hashtag'])

    def test_hashtag_multiple(self):
        result = self.parser.parse(u'text #hashtag1 #hashtag2')
        self.assertEqual(result.html, u'text <a href="http://search.twitter.com/search?q=%23hashtag1">#hashtag1</a> <a href="http://search.twitter.com/search?q=%23hashtag2">#hashtag2</a>')
        self.assertEqual(result.tags, [u'hashtag1', u'hashtag2'])

    def test_not_hashtag_number(self):
        result = self.parser.parse(u'text #1234')
        self.assertEqual(result.html, u'text #1234')
        self.assertEqual(result.tags, [])

    def test_not_hashtag_text(self):
        result = self.parser.parse(u'text#hashtag')
        self.assertEqual(result.html, u'text#hashtag')
        self.assertEqual(result.tags, [])

    def test_hashtag_umlaut(self):
        result = self.parser.parse(u'text #hash_tagüäö')
        self.assertEqual(result.html, u'text <a href="http://search.twitter.com/search?q=%23hash_tag%C3%BC%C3%A4%C3%B6">#hash_tagüäö</a>')
        self.assertEqual(result.tags, [u'hash_tag\xfc\xe4\xf6'])

    def test_hashtag_alpha(self):
        result = self.parser.parse(u'text #hash0tag')
        self.assertEqual(result.html, u'text <a href="http://search.twitter.com/search?q=%23hash0tag">#hash0tag</a>')
        self.assertEqual(result.tags, [u'hash0tag'])

    def test_hashtag_under(self):
        result = self.parser.parse(u'text #hash_tag')
        self.assertEqual(result.html, u'text <a href="http://search.twitter.com/search?q=%23hash_tag">#hash_tag</a>')
        self.assertEqual(result.tags, [u'hash_tag'])

    # Username tests -----------------------------------------------------------
    # --------------------------------------------------------------------------
    def test_not_username_preceded_letter(self):
        result = self.parser.parse(u'meet@the beach')
        self.assertEqual(result.html, u'meet@the beach')
        self.assertEqual(result.users, [])

    def test_username_preceded_punctuation(self):
        result = self.parser.parse(u'.@username')
        self.assertEqual(result.html, u'.<a href="http://twitter.com/username">@username</a>')
        self.assertEqual(result.users, [u'username'])

    def test_username_preceded_japanese(self):
        result = self.parser.parse(u'あ@username')
        self.assertEqual(result.html, u'あ<a href="http://twitter.com/username">@username</a>')
        self.assertEqual(result.users, [u'username'])

    def test_username_followed_japanese(self):
        result = self.parser.parse(u'@usernameの')
        self.assertEqual(result.html, u'<a href="http://twitter.com/username">@username</a>の')
        self.assertEqual(result.users, [u'username'])

    def test_username_surrounded_japanese(self):
        result = self.parser.parse(u'あ@usernameの')
        self.assertEqual(result.html, u'あ<a href="http://twitter.com/username">@username</a>の')
        self.assertEqual(result.users, [u'username'])

    def test_username_followed_punctuation(self):
        result = self.parser.parse(u'@username&^$%^')
        self.assertEqual(result.html, u'<a href="http://twitter.com/username">@username</a>&^$%^')
        self.assertEqual(result.users, [u'username'])

    def test_not_username_spaced(self):
        result = self.parser.parse(u'@ username')
        self.assertEqual(result.html, u'@ username')
        self.assertEqual(result.users, [])

    def test_username_beginning(self):
        result = self.parser.parse(u'@username text')
        self.assertEqual(result.html, u'<a href="http://twitter.com/username">@username</a> text')
        self.assertEqual(result.users, [u'username'])

    def test_username_to_long(self):
        result = self.parser.parse(u'@username9012345678901')
        self.assertEqual(result.html, u'<a href="http://twitter.com/username901234567890">@username901234567890</a>1')
        self.assertEqual(result.users, [u'username901234567890'])

    def test_username_full_at_sign(self):
        result = self.parser.parse(u'＠username')
        self.assertEqual(result.html, u'<a href="http://twitter.com/username">＠username</a>')
        self.assertEqual(result.users, [u'username'])

    def test_username_trailing(self):
        result = self.parser.parse(u'text @username')
        self.assertEqual(result.html, u'text <a href="http://twitter.com/username">@username</a>')
        self.assertEqual(result.users, [u'username'])

    # Replies
    def test_username_reply_simple(self):
        result = self.parser.parse(u'@username')
        self.assertEqual(result.html, u'<a href="http://twitter.com/username">@username</a>')
        self.assertEqual(result.users, [u'username'])
        self.assertEqual(result.reply, u'username')

    def test_username_reply_whitespace(self):
        result = self.parser.parse(u'   @username')
        self.assertEqual(result.html, u'   <a href="http://twitter.com/username">@username</a>')
        self.assertEqual(result.users, [u'username'])
        self.assertEqual(result.reply, u'username')

    def test_username_reply_full(self):
        result = self.parser.parse(u'　@username')
        self.assertEqual(result.html, u'　<a href="http://twitter.com/username">@username</a>')
        self.assertEqual(result.users, [u'username'])
        self.assertEqual(result.reply, u'username')

    def test_username_non_reply(self):
        result = self.parser.parse(u'test @username')
        self.assertEqual(result.html, u'test <a href="http://twitter.com/username">@username</a>')
        self.assertEqual(result.users, [u'username'])
        self.assertEqual(result.reply, None)

    # List tests ---------------------------------------------------------------
    # --------------------------------------------------------------------------
    def test_list_preceeded(self):
        result = self.parser.parse(u'text @username/list')
        self.assertEqual(result.html, u'text <a href="http://twitter.com/username/list">@username/list</a>')
        self.assertEqual(result.lists, [(u'username', u'list')])

    def test_list_beginning(self):
        result = self.parser.parse(u'@username/list')
        self.assertEqual(result.html, u'<a href="http://twitter.com/username/list">@username/list</a>')
        self.assertEqual(result.lists, [(u'username', u'list')])

    def test_list_preceeded_punctuation(self):
        result = self.parser.parse(u'.@username/list')
        self.assertEqual(result.html, u'.<a href="http://twitter.com/username/list">@username/list</a>')
        self.assertEqual(result.lists, [(u'username', u'list')])

    def test_list_followed_punctuation(self):
        result = self.parser.parse(u'@username/list&^$%^')
        self.assertEqual(result.html, u'<a href="http://twitter.com/username/list">@username/list</a>&^$%^')
        self.assertEqual(result.lists, [(u'username', u'list')])

    def test_list_not_slash_space(self):
        result = self.parser.parse(u'@username/ list')
        self.assertEqual(result.html, u'<a href="http://twitter.com/username">@username</a>/ list')
        self.assertEqual(result.users, [u'username'])
        self.assertEqual(result.lists, [])

    def test_list_beginning2(self):
        result = self.parser.parse(u'@username/list')
        self.assertEqual(result.html, u'<a href="http://twitter.com/username/list">@username/list</a>')
        self.assertEqual(result.lists, [(u'username', u'list')])

    def test_list_not_empty_username(self):
        result = self.parser.parse(u'text @/list')
        self.assertEqual(result.html, u'text @/list')
        self.assertEqual(result.lists, [])

    def test_list_not_preceeded_letter(self):
        result = self.parser.parse(u'meet@the/beach')
        self.assertEqual(result.html, u'meet@the/beach')
        self.assertEqual(result.lists, [])

    def test_list_long_truncate(self):
        result = self.parser.parse(u'@username/list5678901234567890123456789012345678901234567890123456789012345678901234567890A')
        self.assertEqual(
            result.html, u'<a href="http://twitter.com/username/list5678901234567890123456789012345678901234567890123456789012345678901234567890">@username/list5678901234567890123456789012345678901234567890123456789012345678901234567890</a>A')
        self.assertEqual(result.lists, [(u'username', u'list5678901234567890123456789012345678901234567890123456789012345678901234567890')])

    def test_list_with_dash(self):
        result = self.parser.parse(u'text @username/list-foo')
        self.assertEqual(result.html, u'text <a href="http://twitter.com/username/list-foo">@username/list-foo</a>')
        self.assertEqual(result.lists, [(u'username', u'list-foo')])


class TWPTestsWithSpans(unittest.TestCase):

    """Test ttp with re spans to extract character co-ords of matches"""
    def setUp(self):
        self.parser = ttp.Parser(include_spans=True)

    def test_spans_in_tweets(self):
        """Test some coca-cola tweets taken from twitter with spans"""
        result = self.parser.parse(u'Coca-Cola Hits 50 Million Facebook Likes http://bit.ly/QlKOc7')
        self.assertEqual(result.urls, [('http://bit.ly/QlKOc7', (41, 61))])

        result = self.parser.parse(u' #ABillionReasonsToBelieveInAfrica ARISE MAG.FASHION WEEK NY! Tsemaye B,Maki Oh,Tiffany Amber, Ozwald.Showin NY reasons2beliv @CocaCola_NG', html=False)
        self.assertEqual(result.urls, [])
        self.assertEqual(result.tags, [(u'ABillionReasonsToBelieveInAfrica', (1, 34))])
        self.assertEqual(result.users, [(u'CocaCola_NG', (126, 138))])

        result = self.parser.parse(u'Follow @CokeZero & Retweet for a chance to win @EASPORTS @EANCAAFootball 13 #GameOn #ad Rules: http://bit.ly/EANCAA', html=False)
        self.assertEqual(result.urls, [(u'http://bit.ly/EANCAA', (95, 115))])
        self.assertEqual(result.users, [(u'CokeZero', (7, 16)), (u'EASPORTS', (47, 56)), (u'EANCAAFootball', (57, 72))])
        self.assertEqual(result.tags, [(u'GameOn', (76, 83)), (u'ad', (84, 87))])

    def test_users_in_tweets(self):
        result = self.parser.parse(u'Follow @CokeZero & Retweet for a chance to win @EASPORTS @EANCAAFootball 13 #GameOn #ad Rules: http://bit.ly/EANCAA @someone', html=False)
        self.assertEqual(result.users, [(u'CokeZero', (7, 16)), (u'EASPORTS', (47, 56)), (u'EANCAAFootball', (57, 72)), (u'someone', (116, 124))])

    def test_edge_cases(self):
        """Some edge cases that upset the original version of ttp"""
        result = self.parser.parse(u' @user', html=False)
        self.assertEqual(result.users, [(u'user', (1, 6))])

        result = self.parser.parse(u' #hash ', html=False)
        self.assertEqual(result.tags, [(u'hash', (1, 6))])

        result = self.parser.parse(u' http://some.com ', html=False)
        self.assertEqual(result.urls, [(u'http://some.com', (1, 16))])


# Test it!
if __name__ == '__main__':
    unittest.main()

    # verbosity = 0 # set to 2 for verbose output
    # suite = unittest.TestLoader().loadTestsFromTestCase(TWPTestsWithSpansEdgeCases)
    # unittest.TextTestRunner(verbosity=verbosity).run(suite)
    # suite = unittest.TestLoader().loadTestsFromTestCase(TWPTestsWithSpans)
    # unittest.TextTestRunner(verbosity=verbosity).run(suite)
    # suite = unittest.TestLoader().loadTestsFromTestCase(TWPTests)
    # unittest.TextTestRunner(verbosity=verbosity).run(suite)
