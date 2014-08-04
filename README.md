twitter-text-python
===================

**twitter-text-python** is a Tweet parser and formatter for Python. Extract
users, hashtags, URLs and format as HTML for display.

PyPI release: [https://pypi.python.org/pypi/twitter-text-python/](http://pypi.python.org/pypi/twitter-text-python/)


installation
------------

    $ pip install twitter-text-python


usage
-----

    >>> from ttp import ttp
    >>> p = ttp.Parser()
    >>> result = p.parse("@burnettedmond, you now support #IvoWertzel's tweet parser! https://github.com/edburnett/")
    >>> result.reply
    'burnettedmond'
    >>> result.users
    ['burnettedmond']
    >>> result.tags
    ['IvoWertzel']
    >>> result.urls
    ['https://github.com/burnettedmond/']
    >>> result.html
    u'<a href="http://twitter.com/burnettedmond">@burnettedmond</a>, you now support <a href="https://twitter.com/search?q=%23IvoWertzel">#IvoWertzel</a>\'s tweet parser! <a href="https://github.com/edburnett/">https://github.com/edburnett/</a>'

If you need different HTML output just subclass and override the `format_*` methods.

You can also ask for the span tags to be returned for each entity:

    >>> p = ttp.Parser(include_spans=True)
    >>> result = p.parse("@burnettedmond, you now support #IvoWertzel's tweet parser! https://github.com/edburnett/")
    >>> result.urls
    [('https://github.com/burnettedmond/', (57, 87))]


To use the shortlink follower

    >>> from ttp import utils
    >>> # assume that result.urls == ['http://t.co/8o0z9BbEMu', u'http://bbc.in/16dClPF']
    >>> print utils.follow_shortlinks(result.urls)  # pass in list of shortlink URLs
    {'http://t.co/8o0z9BbEMu': [u'http://t.co/8o0z9BbEMu', u'http://bbc.in/16dClPF', u'http://www.bbc.co.uk/sport/0/21711199#TWEET650562'], u'http://bbc.in/16dClPF': [u'http://bbc.in/16dClPF', u'http://www.bbc.co.uk/sport/0/21711199#TWEET650562']}
     >>> # note that bad shortlink URLs have a key to an empty list (lost/forgotten shortlink URLs don't generate any error)


changelog
---------

* 2014/7/30 1.0.3 Update parsed URLs for Twitter API 1.1 compatibility
* 2013/6/1 1.0.1 new working version, adding comma parse fix (thanks https://github.com/muckrack), used autopep8 to clean the src, added a shortlink expander
* 2013/2/11 1.0.0.2 released to PyPI


tests
-----

Checkout the code via github https://github.com/edburnett/twitter-text-python and run tests locally::

    $ python ttp/tests.py 
    ....................................................................................................
    ----------------------------------------------------------------------
    Ran 100 tests in 0.009s
    OK


contributing
------------

The source is available on
[https://github.com/edburnett/twitter-text-python](GitHub), to contribute to
the project, fork it on GitHub and send a pull request. Everyone is welcome to
make improvements to **twitter-text-python**!

https://github.com/edburnett/twitter-text-python


history
-------

The current version was forked by Edmond Burnett in July 2014:
https://github.com/edburnett/twitter-text-python

The library was forked by Ian Ozsvald in January 2013 and released to PyPI, some bugs were fixed, a few minor changes to functionality added (no longer supported):
https://github.com/ianozsvald/twitter-text-python

The original ttp comes from Ivo Wetzel (no longer supported):
https://github.com/BonsaiDen/twitter-text-python

Originally based on [http://github.com/mzsanford/twitter-text-java](twitter-text-java).


license
-------

*MIT*

Copyright (c) 2012 Ivo Wetzel.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Copyright (c) 2010-2013 Ivo Wetzel

