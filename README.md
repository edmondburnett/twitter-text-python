instagram-text-python
===================

**instagram-text-python** is a Tweet parser and formatter for Python. Extract
users, hashtags, URLs and format as HTML for display.

PyPI release: [https://pypi.python.org/pypi/instagram-text-python/](http://pypi.python.org/pypi/instagram-text-python/)


installation
------------

    $ pip install instagram-text-python


compatibility
-------------

instagram-text-python supports Python 2.6, 2.7, 3.3, 3.4 and 3.5.


usage
-----

```python
>>> from itp import itp
>>> p = itp.Parser()
>>> result = p.parse("Hey @user.name, you now support the #itp parser! https://github.com/takumihq")
>>> result.reply
'user.name'
>>> result.users
['user.name']
>>> result.tags
['itp']
>>> result.urls
['https://github.com/takumihq/']
>>> result.html
u'<a href="http://instagram.com/user.name">@user.name</a>, you now support the <a href="https://www.instagram.com/explore/tags/itp/">#itp</a> parser! <a href="https://github.com/takumihq/">https://github.com/takumihq/</a>'
```

If you need different HTML output just subclass and override the `format_*` methods.

You can also ask for the span tags to be returned for each entity:

```python
>>> p = itp.Parser(include_spans=True)
>>> result = p.parse("Hey @user.name, you now support the #itp parser! https://github.com/takumihq")
>>> result.urls
[('https://github.com/takumihq/', (57, 87))]
```


To use the shortlink follower (depends on the [Requests](http://docs.python-requests.org/) library):

```python
>>> from itp import utils
>>> # assume that result.urls == ['http://t.co/8o0z9BbEMu', u'http://bbc.in/16dClPF']
>>> print utils.follow_shortlinks(result.urls)  # pass in list of shortlink URLs
{'http://t.co/8o0z9BbEMu': [u'http://t.co/8o0z9BbEMu', u'http://bbc.in/16dClPF', u'http://www.bbc.co.uk/sport/0/21711199#TWEET650562'], u'http://bbc.in/16dClPF': [u'http://bbc.in/16dClPF', u'http://www.bbc.co.uk/sport/0/21711199#TWEET650562']}
 >>> # note that bad shortlink URLs have a key to an empty list (lost/forgotten shortlink URLs don't generate any error)
```


changelog
---------

* 2016/03/08 2.0.0 Forked [ttp](https://github.com/edburnett/twitter-text-python) to become an instagram text parser
* 2015/04/11 1.1.0 Add basic support for Python 3
* 2014/07/30 1.0.3 Update parsed URLs for twitter API 1.1 compatibility
* 2013/06/01 1.0.1 new working version, adding comma parse fix (thanks https://github.com/muckrack), used autopep8 to clean the src, added a shortlink expander
* 2013/02/11 1.0.0.2 released to PyPI


tests
-----

Run the unit tests:

    $ python itp/tests.py
    ....................................................................................................
    ----------------------------------------------------------------------
    Ran 100 tests in 0.009s
    OK

Or test on multiple Python versions with tox:

    $ pip install tox
    $ tox


contributing
------------

See the relevant [wiki
page](https://github.com/edburnett/instagram-text-python/wiki/Contributing) for
notes on contributing to **instagram-text-python**.


history
-------

The current version was forked by TakumiHQ in March 2016 and modified to
support instagram text parsings instead of twitter:
https://github.com/takumihq/instagram-text-python

The library won was forked by Edmond Burnett in July 2014:
https://github.com/edburnett/twitter-text-python

The library was forked by Ian Ozsvald in January 2013 and released to PyPI,
some bugs were fixed, a few minor changes to functionality added (no longer
supported): https://github.com/ianozsvald/twitter-text-python

The original itp comes from Ivo Wetzel (no longer supported):
https://github.com/BonsaiDen/twitter-text-python

Originally based on
[https://github.com/mzsanford/twitter-text-java](https://github.com/mzsanford/twitter-text-java).


license
-------

The MIT License (MIT)

Copyright (c) 2012-2013 Ivo Wetzel.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
