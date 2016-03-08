# -*- coding: UTF-8 -*-
#  This file is part of instagram-text-python.
#
#  The MIT License (MIT)
#
#  Copyright (c) 2012-2013 Ivo Wetzel
#
#  twitter-text-python is free software: you can redistribute it and/or
#  modify it under the terms of the MIT License.
#
#  You should have received a copy of the MIT License along with
#  twitter-text-python. If not, see <http://opensource.org/licenses/MIT>.
#
#  Maintained by Takumi:
#  https://github.com/takumihq/instagram-text-python
#  (previously Edmond Burnett, Ian Ozsvald and Ivo Wetzel)


# twp - Unittests -------------------------------------------------------------
# -----------------------------------------------------------------------------
from __future__ import unicode_literals
import unittest
import itp


class TWPTests(unittest.TestCase):

    def setUp(self):
        self.parser = itp.Parser()

    # General Tests -----------------------------------------------------------
    # -------------------------------------------------------------------------
    def test_urls(self):
        """Confirm that # in a URL works along with ,"""
        result = self.parser.parse('big url: http://blah.com:8080/path/to/here?p=1&q=abc,def#posn2 #ahashtag')
        self.assertEqual(result.urls, ['http://blah.com:8080/path/to/here?p=1&q=abc,def#posn2'])
        self.assertEqual(result.tags, ['ahashtag'])

    def test_all_not_allow_amp_without_question(self):
        result = self.parser.parse('Check out: http://www.github.com/test&@username')
        self.assertEqual(result.html, (
            'Check out: <a href="http://www.github.com/test">http://www.github.com/test</a>&'
            '<a href="https://instagram.com/username">@username</a>'
        ))
        self.assertEqual(result.users, ['username'])
        self.assertEqual(result.urls, ['http://www.github.com/test'])

    def test_all_not_break_url_at(self):
        result = self.parser.parse('http://www.flickr.com/photos/29674651@N00/4382024406')
        self.assertEqual(
            result.html,
            '<a href="http://www.flickr.com/photos/29674651@N00/4382024406">http://www.flickr.com/photo...</a>'
        )
        self.assertEqual(result.urls, ['http://www.flickr.com/photos/29674651@N00/4382024406'])

    # URL tests ----------------------------------------------------------------
    # --------------------------------------------------------------------------
    def test_url_mid(self):
        result = self.parser.parse('text http://example.com more text')
        self.assertEqual(result.html, 'text <a href="http://example.com">http://example.com</a> more text')
        self.assertEqual(result.urls, ['http://example.com'])

    def test_url_unicode(self):
        result = self.parser.parse('I enjoy Macintosh Brand computers: http://✪df.ws/ejp')
        self.assertEqual(
            result.html, 'I enjoy Macintosh Brand computers: <a href="http://✪df.ws/ejp">http://✪df.ws/ejp</a>')
        self.assertEqual(result.urls, ['http://\u272adf.ws/ejp'])

    def test_url_parentheses(self):
        result = self.parser.parse('text (http://example.com)')
        self.assertEqual(result.html, 'text (<a href="http://example.com">http://example.com</a>)')
        self.assertEqual(result.urls, ['http://example.com'])

    def test_url_underscore(self):
        result = self.parser.parse('text http://example.com/test/foo_123.jpg')
        self.assertEqual(
            result.html, 'text <a href="http://example.com/test/foo_123.jpg">http://example.com/test/foo...</a>')
        self.assertEqual(result.urls, ['http://example.com/test/foo_123.jpg'])

    def test_url_underscore_dot(self):
        result = self.parser.parse('text http://example.com/test/bla.net_foo_123.jpg')
        self.assertEqual(
            result.html,
            'text <a href="http://example.com/test/bla.net_foo_123.jpg">http://example.com/test/bla...</a>')
        self.assertEqual(result.urls, ['http://example.com/test/bla.net_foo_123.jpg'])

    def test_url_amp_lang_equals(self):
        result = self.parser.parse('Check out https://twitter.com/search?q=avro&lang=en')
        self.assertEqual(
            result.html,
            'Check out <a href="https://twitter.com/search?q=avro&amp;lang=en">https://twitter.com/search?...</a>'
        )
        self.assertEqual(result.urls, ['https://twitter.com/search?q=avro&lang=en'])

    def test_url_amp_break(self):
        result = self.parser.parse('Check out http://twitter.com/te?foo&invalid=True')
        self.assertEqual(
            result.html,
            'Check out <a href="http://twitter.com/te?foo&amp;invalid=True">http://twitter.com/te?foo...</a>'
        )
        self.assertEqual(result.urls, ['http://twitter.com/te?foo&invalid=True'])

    def test_url_dash(self):
        result = self.parser.parse('Is www.foo-bar.com a valid URL?')
        self.assertEqual(result.html, 'Is <a href="https://www.foo-bar.com">www.foo-bar.com</a> a valid URL?')
        self.assertEqual(result.urls, ['www.foo-bar.com'])

    def test_url_multiple(self):
        result = self.parser.parse('http://example.com https://sslexample.com http://sub.example.com')
        self.assertEqual(result.html, (
            '<a href="http://example.com">http://example.com</a> <a href="https://sslexample.com">'
            'https://sslexample.com</a> <a href="http://sub.example.com">http://sub.example.com</a>'
        ))
        self.assertEqual(result.urls, ['http://example.com', 'https://sslexample.com', 'http://sub.example.com'])

    def test_url_raw_domain(self):
        result = self.parser.parse('See http://example.com example.com')
        self.assertEqual(result.html, 'See <a href="http://example.com">http://example.com</a> example.com')
        self.assertEqual(result.urls, ['http://example.com'])

    def test_url_embed_link(self):
        result = self.parser.parse('<link rel=\'true\'>http://example.com</link>')
        self.assertEqual(result.html, '<link rel=\'true\'><a href="http://example.com">http://example.com</a></link>')
        self.assertEqual(result.urls, ['http://example.com'])

    def test_url_trailing(self):
        result = self.parser.parse('text http://example.com')
        self.assertEqual(result.html, 'text <a href="http://example.com">http://example.com</a>')
        self.assertEqual(result.urls, ['http://example.com'])

    def test_url_japanese(self):
        result = self.parser.parse('いまなにしてるhttp://example.comいまなにしてる')
        self.assertEqual(result.html, 'いまなにしてる<a href="http://example.com">http://example.com</a>いまなにしてる')
        self.assertEqual(result.urls, ['http://example.com'])

    def test_url_lots_of_punctuation(self):
        result = self.parser.parse('text http://xo.com/~matthew+%-,.;x')
        self.assertEqual(result.html, 'text <a href="http://xo.com/~matthew+%-,.;x">http://xo.com/~matthew+%-,.;x</a>')
        self.assertEqual(result.urls, ['http://xo.com/~matthew+%-,.;x'])

    def test_url_question_numbers(self):
        result = self.parser.parse('text http://example.com/?77e8fd')
        self.assertEqual(result.html, 'text <a href="http://example.com/?77e8fd">http://example.com/?77e8fd</a>')
        self.assertEqual(result.urls, ['http://example.com/?77e8fd'])

    def test_url_one_letter_other(self):
        result = self.parser.parse('text http://u.nu/')
        self.assertEqual(result.html, 'text <a href="http://u.nu/">http://u.nu/</a>')
        self.assertEqual(result.urls, ['http://u.nu/'])

        result = self.parser.parse('text http://u.tv/')
        self.assertEqual(result.html, 'text <a href="http://u.tv/">http://u.tv/</a>')
        self.assertEqual(result.urls, ['http://u.tv/'])

    def test_url_one_letter_iana(self):
        result = self.parser.parse('text http://x.com/')
        self.assertEqual(result.html, 'text <a href="http://x.com/">http://x.com/</a>')
        self.assertEqual(result.urls, ['http://x.com/'])

        result = self.parser.parse('text http://Q.com/')
        self.assertEqual(result.html, 'text <a href="http://Q.com/">http://Q.com/</a>')
        self.assertEqual(result.urls, ['http://Q.com/'])

        result = self.parser.parse('text http://z.com/')
        self.assertEqual(result.html, 'text <a href="http://z.com/">http://z.com/</a>')
        self.assertEqual(result.urls, ['http://z.com/'])

        result = self.parser.parse('text http://i.net/')
        self.assertEqual(result.html, 'text <a href="http://i.net/">http://i.net/</a>')
        self.assertEqual(result.urls, ['http://i.net/'])

        result = self.parser.parse('text http://q.net/')
        self.assertEqual(result.html, 'text <a href="http://q.net/">http://q.net/</a>')
        self.assertEqual(result.urls, ['http://q.net/'])

        result = self.parser.parse('text http://X.org/')
        self.assertEqual(result.html, 'text <a href="http://X.org/">http://X.org/</a>')
        self.assertEqual(result.urls, ['http://X.org/'])

    def test_url_long_hypens(self):
        result = self.parser.parse('text http://word-and-a-number-8-ftw.domain.tld/')
        self.assertEqual(
            result.html,
            'text <a href="http://word-and-a-number-8-ftw.domain.tld/">http://word-and-a-number-8-...</a>'
        )
        self.assertEqual(result.urls, ['http://word-and-a-number-8-ftw.domain.tld/'])

    # URL not tests ------------------------------------------------------------
    def test_not_url_dotdotdot(self):
        result = self.parser.parse('Is www...foo a valid URL?')
        self.assertEqual(result.html, 'Is www...foo a valid URL?')
        self.assertEqual(result.urls, [])

    def test_not_url_dash(self):
        result = self.parser.parse('Is www.-foo.com a valid URL?')
        self.assertEqual(result.html, 'Is www.-foo.com a valid URL?')
        self.assertEqual(result.urls, [])

    def test_not_url_no_tld(self):
        result = self.parser.parse('Is http://no-tld a valid URL?')
        self.assertEqual(result.html, 'Is http://no-tld a valid URL?')
        self.assertEqual(result.urls, [])

    def test_not_url_tld_too_short(self):
        result = self.parser.parse('Is http://tld-too-short.x a valid URL?')
        self.assertEqual(result.html, 'Is http://tld-too-short.x a valid URL?')
        self.assertEqual(result.urls, [])

    def test_all_not_break_url_at2(self):
        result = self.parser.parse('http://www.flickr.com/photos/29674651@N00/4382024406')
        self.assertEqual(
            result.html,
            '<a href="http://www.flickr.com/photos/29674651@N00/4382024406">http://www.flickr.com/photo...</a>'
        )
        self.assertEqual(result.urls, ['http://www.flickr.com/photos/29674651@N00/4382024406'])

    def test_not_url_one_letter_iana(self):
        result = self.parser.parse('text http://a.com/ http://a.net/ http://a.org/')
        self.assertEqual(result.html, 'text http://a.com/ http://a.net/ http://a.org/')
        self.assertEqual(result.urls, [])

    # URL followed Tests -------------------------------------------------------
    def test_url_followed_question(self):
        result = self.parser.parse('text http://example.com?')
        self.assertEqual(result.html, 'text <a href="http://example.com">http://example.com</a>?')
        self.assertEqual(result.urls, ['http://example.com'])

    def test_url_followed_colon(self):
        result = self.parser.parse('text http://example.com:')
        self.assertEqual(result.html, 'text <a href="http://example.com">http://example.com</a>:')
        self.assertEqual(result.urls, ['http://example.com'])

    def test_url_followed_curly_brace(self):
        result = self.parser.parse('text http://example.com}')
        self.assertEqual(result.html, 'text <a href="http://example.com">http://example.com</a>}')
        self.assertEqual(result.urls, ['http://example.com'])

    def test_url_followed_single_quote(self):
        result = self.parser.parse('text http://example.com')
        self.assertEqual(result.html, 'text <a href="http://example.com">http://example.com</a>')
        self.assertEqual(result.urls, ['http://example.com'])

    def test_url_followed_dot(self):
        result = self.parser.parse('text http://example.com.')
        self.assertEqual(result.html, 'text <a href="http://example.com">http://example.com</a>.')
        self.assertEqual(result.urls, ['http://example.com'])

    def test_url_followed_exclamation(self):
        result = self.parser.parse('text http://example.com!')
        self.assertEqual(result.html, 'text <a href="http://example.com">http://example.com</a>!')
        self.assertEqual(result.urls, ['http://example.com'])

    def test_url_followed_comma(self):
        result = self.parser.parse('text http://example.com,')
        self.assertEqual(result.html, 'text <a href="http://example.com">http://example.com</a>,')
        self.assertEqual(result.urls, ['http://example.com'])

    def test_url_with_path_preceeded_by_comma(self):
        result = self.parser.parse('text ,http://example.com/abcde, more')
        self.assertEqual(result.html, 'text ,<a href="http://example.com/abcde">http://example.com/abcde</a>, more')
        self.assertEqual(result.urls, ['http://example.com/abcde'])

    def test_url_with_path_followed_comma(self):
        result = self.parser.parse('text http://example.com/abcde, more')
        self.assertEqual(result.html, 'text <a href="http://example.com/abcde">http://example.com/abcde</a>, more')
        self.assertEqual(result.urls, ['http://example.com/abcde'])

    def test_url_with_path_followed_commas(self):
        result = self.parser.parse('text http://example.com/abcde,, more')
        self.assertEqual(result.html, 'text <a href="http://example.com/abcde">http://example.com/abcde</a>,, more')
        self.assertEqual(result.urls, ['http://example.com/abcde'])

    def test_url_followed_brace(self):
        result = self.parser.parse('text http://example.com)')
        self.assertEqual(result.html, 'text <a href="http://example.com">http://example.com</a>)')
        self.assertEqual(result.urls, ['http://example.com'])

    def test_url_followed_big_brace(self):
        result = self.parser.parse('text http://example.com]')
        self.assertEqual(result.html, 'text <a href="http://example.com">http://example.com</a>]')
        self.assertEqual(result.urls, ['http://example.com'])

    def test_url_followed_equals(self):
        result = self.parser.parse('text http://example.com=')
        self.assertEqual(result.html, 'text <a href="http://example.com">http://example.com</a>=')
        self.assertEqual(result.urls, ['http://example.com'])

    def test_url_followed_semicolon(self):
        result = self.parser.parse('text http://example.com;')
        self.assertEqual(result.html, 'text <a href="http://example.com">http://example.com</a>;')
        self.assertEqual(result.urls, ['http://example.com'])

    def test_url_followed_hypen(self):
        result = self.parser.parse('text http://domain.tld-that-you-should-have-put-a-space-after')
        self.assertEqual(
            result.html,
            'text <a href="http://domain.tld">http://domain.tld</a>-that-you-should-have-put-a-space-after'
        )
        self.assertEqual(result.urls, ['http://domain.tld'])

    # URL preceeded Tests -------------------------------------------------------
    def test_url_preceeded_colon(self):
        result = self.parser.parse('text:http://example.com')
        self.assertEqual(result.html, 'text:<a href="http://example.com">http://example.com</a>')
        self.assertEqual(result.urls, ['http://example.com'])

    def test_not_url_preceeded_equals(self):
        result = self.parser.parse('text =http://example.com')
        self.assertEqual(result.html, 'text =http://example.com')
        self.assertEqual(result.urls, [])

    # NOT
    def test_not_url_preceeded_forwardslash(self):
        result = self.parser.parse('text /http://example.com')
        self.assertEqual(result.html, 'text /http://example.com')
        self.assertEqual(result.urls, [])

    def test_not_url_preceeded_exclamation(self):
        result = self.parser.parse('text !http://example.com')
        self.assertEqual(result.html, 'text !http://example.com')
        self.assertEqual(result.urls, [])

    # URL numeric tests --------------------------------------------------------
    def test_url_at_numeric(self):
        result = self.parser.parse('http://www.flickr.com/photos/29674651@N00/4382024406')
        self.assertEqual(
            result.html,
            '<a href="http://www.flickr.com/photos/29674651@N00/4382024406">http://www.flickr.com/photo...</a>'
        )
        self.assertEqual(result.urls, ['http://www.flickr.com/photos/29674651@N00/4382024406'])

    def test_url_at_non_numeric(self):
        result = self.parser.parse('http://www.flickr.com/photos/29674651@N00/foobar')
        self.assertEqual(
            result.html,
            '<a href="http://www.flickr.com/photos/29674651@N00/foobar">http://www.flickr.com/photo...</a>'
        )
        self.assertEqual(result.urls, ['http://www.flickr.com/photos/29674651@N00/foobar'])

    # URL domain tests ---------------------------------------------------------
    def test_url_WWW(self):
        result = self.parser.parse('WWW.EXAMPLE.COM')
        self.assertEqual(result.html, '<a href="https://WWW.EXAMPLE.COM">WWW.EXAMPLE.COM</a>')
        self.assertEqual(result.urls, ['WWW.EXAMPLE.COM'])

    def test_url_www(self):
        result = self.parser.parse('www.example.com')
        self.assertEqual(result.html, '<a href="https://www.example.com">www.example.com</a>')
        self.assertEqual(result.urls, ['www.example.com'])

    def test_url_only_domain_query_followed_period(self):
        result = self.parser.parse((
            'I think it\'s proper to end sentences with a period '
            'http://tell.me/why?=because.i.want.it. Even when they contain a URL.')
        )
        self.assertEqual(result.html, (
            'I think it\'s proper to end sentences with a period <a href="http://tell.me/why?=because.i.want.it">'
            'http://tell.me/why?=because...</a>. Even when they contain a URL.'
        ))
        self.assertEqual(result.urls, ['http://tell.me/why?=because.i.want.it'])

    def test_url_only_domain_followed_period(self):
        result = self.parser.parse(
            'I think it\'s proper to end sentences with a period http://tell.me. Even when they contain a URL.')
        self.assertEqual(result.html, (
            'I think it\'s proper to end sentences with a period <a href="http://tell.me">http://tell.me</a>. '
            'Even when they contain a URL.'
        ))
        self.assertEqual(result.urls, ['http://tell.me'])

    def test_url_only_domain_path_followed_period(self):
        result = self.parser.parse(
            'I think it\'s proper to end sentences with a period http://tell.me/why. Even when they contain a URL.')
        self.assertEqual(result.html, (
            'I think it\'s proper to end sentences with a period <a href="http://tell.me/why">http://tell.me/why</a>.'
            ' Even when they contain a URL.'
        ))
        self.assertEqual(result.urls, ['http://tell.me/why'])

    def test_url_long_tld(self):
        result = self.parser.parse('http://example.mobi/path')
        self.assertEqual(result.html, '<a href="http://example.mobi/path">http://example.mobi/path</a>')
        self.assertEqual(result.urls, ['http://example.mobi/path'])

    def test_url_multiple_protocols(self):
        result = self.parser.parse('http://foo.com AND https://bar.com AND www.foobar.com')
        self.assertEqual(result.html, (
            '<a href="http://foo.com">http://foo.com</a> AND <a href="https://bar.com">'
            'https://bar.com</a> AND <a href="https://www.foobar.com">www.foobar.com</a>'
        ))
        self.assertEqual(result.urls, ['http://foo.com', 'https://bar.com', 'www.foobar.com'])

    # NOT
    def test_not_url_exclamation_domain(self):
        result = self.parser.parse('badly formatted http://foo!bar.com')
        self.assertEqual(result.html, 'badly formatted http://foo!bar.com')
        self.assertEqual(result.urls, [])

    def test_not_url_under_domain(self):
        result = self.parser.parse('badly formatted http://foo_bar.com')
        self.assertEqual(result.html, 'badly formatted http://foo_bar.com')
        self.assertEqual(result.urls, [])

    # Hashtag tests ------------------------------------------------------------
    # --------------------------------------------------------------------------
    def test_hashtag_followed_full_whitespace(self):
        result = self.parser.parse('#hashtag　text')
        self.assertEqual(result.html, '<a href="https://instagram.com/explore/tags/hashtag/">#hashtag</a>　text')
        self.assertEqual(result.tags, ['hashtag'])

    def test_hashtag_followed_full_hash(self):
        result = self.parser.parse('＃hashtag')
        self.assertEqual(result.html, '<a href="https://instagram.com/explore/tags/hashtag/">＃hashtag</a>')
        self.assertEqual(result.tags, ['hashtag'])

    def test_hashtag_preceeded_full_whitespace(self):
        result = self.parser.parse('text　#hashtag')
        self.assertEqual(result.html, 'text　<a href="https://instagram.com/explore/tags/hashtag/">#hashtag</a>')
        self.assertEqual(result.tags, ['hashtag'])

    def test_hashtag_number(self):
        result = self.parser.parse('text #1tag')
        self.assertEqual(result.html, 'text <a href="https://instagram.com/explore/tags/1tag/">#1tag</a>')
        self.assertEqual(result.tags, ['1tag'])

    def test_not_hashtag_escape(self):
        result = self.parser.parse('&#nbsp;')
        self.assertEqual(result.html, '&#nbsp;')
        self.assertEqual(result.tags, [])

    def test_hashtag_japanese(self):
        result = self.parser.parse('text #hashtagの')
        self.assertEqual(result.html, 'text <a href="https://instagram.com/explore/tags/hashtag/">#hashtag</a>の')
        self.assertEqual(result.tags, ['hashtag'])

    def test_hashtag_period(self):
        result = self.parser.parse('text.#hashtag')
        self.assertEqual(result.html, 'text.<a href="https://instagram.com/explore/tags/hashtag/">#hashtag</a>')
        self.assertEqual(result.tags, ['hashtag'])

    def test_hashtag_trailing(self):
        result = self.parser.parse('text #hashtag')
        self.assertEqual(result.html, 'text <a href="https://instagram.com/explore/tags/hashtag/">#hashtag</a>')
        self.assertEqual(result.tags, ['hashtag'])

    def test_not_hashtag_exclamation(self):
        result = self.parser.parse('text #hashtag!')
        self.assertEqual(result.html, 'text <a href="https://instagram.com/explore/tags/hashtag/">#hashtag</a>!')
        self.assertEqual(result.tags, ['hashtag'])

    def test_hashtag_multiple(self):
        result = self.parser.parse('text #hashtag1 #hashtag2')
        self.assertEqual(result.html, (
            'text <a href="https://instagram.com/explore/tags/hashtag1/">#hashtag1</a> '
            '<a href="https://instagram.com/explore/tags/hashtag2/">#hashtag2</a>'
        ))
        self.assertEqual(result.tags, ['hashtag1', 'hashtag2'])

    def test_not_hashtag_number(self):
        result = self.parser.parse('text #1234')
        self.assertEqual(result.html, 'text #1234')
        self.assertEqual(result.tags, [])

    def test_not_hashtag_text(self):
        result = self.parser.parse('text#hashtag')
        self.assertEqual(result.html, 'text#hashtag')
        self.assertEqual(result.tags, [])

    def test_hashtag_umlaut(self):
        result = self.parser.parse('text #hash_tagüäö')
        self.assertEqual(
            result.html,
            'text <a href="https://instagram.com/explore/tags/hash_tag%C3%BC%C3%A4%C3%B6/">#hash_tagüäö</a>'
        )
        self.assertEqual(result.tags, ['hash_tag\xfc\xe4\xf6'])

    def test_hashtag_alpha(self):
        result = self.parser.parse('text #hash0tag')
        self.assertEqual(result.html, 'text <a href="https://instagram.com/explore/tags/hash0tag/">#hash0tag</a>')
        self.assertEqual(result.tags, ['hash0tag'])

    def test_hashtag_under(self):
        result = self.parser.parse('text #hash_tag')
        self.assertEqual(result.html, 'text <a href="https://instagram.com/explore/tags/hash_tag/">#hash_tag</a>')
        self.assertEqual(result.tags, ['hash_tag'])

    # Username tests -----------------------------------------------------------
    # --------------------------------------------------------------------------
    def test_not_username_preceded_letter(self):
        result = self.parser.parse('meet@the beach')
        self.assertEqual(result.html, 'meet@the beach')
        self.assertEqual(result.users, [])

    def test_username_preceded_punctuation(self):
        result = self.parser.parse('.@username')
        self.assertEqual(result.html, '.<a href="https://instagram.com/username">@username</a>')
        self.assertEqual(result.users, ['username'])

    def test_username_preceded_japanese(self):
        result = self.parser.parse('あ@username')
        self.assertEqual(result.html, 'あ<a href="https://instagram.com/username">@username</a>')
        self.assertEqual(result.users, ['username'])

    def test_username_followed_japanese(self):
        result = self.parser.parse('@usernameの')
        self.assertEqual(result.html, '<a href="https://instagram.com/username">@username</a>の')
        self.assertEqual(result.users, ['username'])

    def test_username_surrounded_japanese(self):
        result = self.parser.parse('あ@usernameの')
        self.assertEqual(result.html, 'あ<a href="https://instagram.com/username">@username</a>の')
        self.assertEqual(result.users, ['username'])

    def test_username_followed_punctuation(self):
        result = self.parser.parse('@username&^$%^')
        self.assertEqual(result.html, '<a href="https://instagram.com/username">@username</a>&^$%^')
        self.assertEqual(result.users, ['username'])

    def test_not_username_spaced(self):
        result = self.parser.parse('@ username')
        self.assertEqual(result.html, '@ username')
        self.assertEqual(result.users, [])

    def test_username_beginning(self):
        result = self.parser.parse('@username text')
        self.assertEqual(result.html, '<a href="https://instagram.com/username">@username</a> text')
        self.assertEqual(result.users, ['username'])

    def test_username_to_long(self):
        return
        result = self.parser.parse('@username9012345678901')
        self.assertEqual(result.html, '<a href="https://instagram.com/username901234567890">@username901234567890</a>1')
        self.assertEqual(result.users, ['username901234567890'])

    def test_username_full_at_sign(self):
        result = self.parser.parse('＠username')
        self.assertEqual(result.html, '<a href="https://instagram.com/username">＠username</a>')
        self.assertEqual(result.users, ['username'])

    def test_username_trailing(self):
        result = self.parser.parse('text @username')
        self.assertEqual(result.html, 'text <a href="https://instagram.com/username">@username</a>')
        self.assertEqual(result.users, ['username'])

    def test_username_dots(self):
        result = self.parser.parse('text @user.name')
        self.assertEqual(result.html, 'text <a href="https://instagram.com/user.name">@user.name</a>')
        self.assertEqual(result.users, ['user.name'])

    # Replies
    def test_username_reply_simple(self):
        result = self.parser.parse('@username')
        self.assertEqual(result.html, '<a href="https://instagram.com/username">@username</a>')
        self.assertEqual(result.users, ['username'])
        self.assertEqual(result.reply, 'username')

    def test_username_reply_whitespace(self):
        result = self.parser.parse('   @username')
        self.assertEqual(result.html, '   <a href="https://instagram.com/username">@username</a>')
        self.assertEqual(result.users, ['username'])
        self.assertEqual(result.reply, 'username')

    def test_username_reply_full(self):
        result = self.parser.parse('　@username')
        self.assertEqual(result.html, '　<a href="https://instagram.com/username">@username</a>')
        self.assertEqual(result.users, ['username'])
        self.assertEqual(result.reply, 'username')

    def test_username_non_reply(self):
        result = self.parser.parse('test @username')
        self.assertEqual(result.html, 'test <a href="https://instagram.com/username">@username</a>')
        self.assertEqual(result.users, ['username'])
        self.assertEqual(result.reply, None)


class TWPTestsWithSpans(unittest.TestCase):

    """Test itp with re spans to extract character co-ords of matches"""
    def setUp(self):
        self.parser = itp.Parser(include_spans=True)

    def test_spans_in_tweets(self):
        """Test some coca-cola tweets taken from twitter with spans"""
        result = self.parser.parse('Coca-Cola Hits 50 Million Facebook Likes http://bit.ly/QlKOc7')
        self.assertEqual(result.urls, [('http://bit.ly/QlKOc7', (41, 61))])

        result = self.parser.parse((
            ' #ABillionReasonsToBelieveInAfrica ARISE MAG.FASHION WEEK NY! Tsemaye B,Maki Oh,Tiffany Amber, '
            'Ozwald.Showin NY reasons2beliv @CocaCola_NG'), html=False)
        self.assertEqual(result.urls, [])
        self.assertEqual(result.tags, [('ABillionReasonsToBelieveInAfrica', (1, 34))])
        self.assertEqual(result.users, [('CocaCola_NG', (126, 138))])

        result = self.parser.parse((
            'Follow @CokeZero & Retweet for a chance to win @EASPORTS @EANCAAFootball 13 #GameOn #ad Rules: '
            'http://bit.ly/EANCAA'), html=False)
        self.assertEqual(result.urls, [('http://bit.ly/EANCAA', (95, 115))])
        self.assertEqual(result.users, [('CokeZero', (7, 16)), ('EASPORTS', (47, 56)), ('EANCAAFootball', (57, 72))])
        self.assertEqual(result.tags, [('GameOn', (76, 83)), ('ad', (84, 87))])

    def test_users_in_tweets(self):
        result = self.parser.parse((
            'Follow @CokeZero & Retweet for a chance to win @EASPORTS @EANCAAFootball 13 #GameOn #ad Rules: '
            'http://bit.ly/EANCAA @someone'), html=False)
        self.assertEqual(result.users, [
            ('CokeZero', (7, 16)), ('EASPORTS', (47, 56)), ('EANCAAFootball', (57, 72)), ('someone', (116, 124))
        ])

    def test_edge_cases(self):
        """Some edge cases that upset the original version of itp"""
        result = self.parser.parse(' @user', html=False)
        self.assertEqual(result.users, [('user', (1, 6))])

        result = self.parser.parse(' #hash ', html=False)
        self.assertEqual(result.tags, [('hash', (1, 6))])

        result = self.parser.parse(' http://some.com ', html=False)
        self.assertEqual(result.urls, [('http://some.com', (1, 16))])


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
