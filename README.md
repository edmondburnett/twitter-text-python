[![CircleCI](https://flat.badgen.net/circleci/github/edmondburnett/twitter-text-python)](https://circleci.com/gh/edmondburnett/twitter-text-python) [![PyPI version](https://flat.badgen.net/pypi/v/twitter-text-python)](https://pypi.org/project/twitter-text-python/)


twitter-text-python
===================

**twitter-text-python** is a Tweet parser and formatter for Python. Extract
users, hashtags, URLs and format as HTML for display.

PyPI release: [https://pypi.org/project/twitter-text-python/](https://pypi.org/project/twitter-text-python/)


installation
------------

    $ pip install twitter-text-python


compatibility
-------------

twitter-text-python has been tested with Python 2.6, 2.7, 3.3, 3.4, 3.5, and 3.7.


usage
-----

```python
>>> from ttp import ttp
>>> p = ttp.Parser()
>>> result = p.parse("@burnettedmond, you now support #IvoWertzel's tweet parser! https://github.com/edmondburnett/")
>>> result.reply
'burnettedmond'
>>> result.users
['burnettedmond']
>>> result.tags
['IvoWertzel']
>>> result.urls
['https://github.com/edmondburnett/']
>>> result.html
u'<a href="http://twitter.com/burnettedmond">@burnettedmond</a>, you now support <a href="https://twitter.com/search?q=%23IvoWertzel">#IvoWertzel</a>\'s tweet parser! <a href="https://github.com/edmondburnett/">https://github.com/edmondburnett/</a>'
```

If you need different HTML output just subclass and override the `format_*` methods.

You can also ask for the span tags to be returned for each entity:

```python
>>> p = ttp.Parser(include_spans=True)
>>> result = p.parse("@burnettedmond, you now support #IvoWertzel's tweet parser! https://github.com/edmondburnett/")
>>> result.urls
[('https://github.com/edmondburnett/', (57, 87))]
```


To use the shortlink follower (depends on the [Requests](http://docs.python-requests.org/) library):

```python
>>> from ttp import utils
>>> # assume that result.urls == ['http://t.co/8o0z9BbEMu', u'http://bbc.in/16dClPF']
>>> print utils.follow_shortlinks(result.urls)  # pass in list of shortlink URLs
{'http://t.co/8o0z9BbEMu': [u'http://t.co/8o0z9BbEMu', u'http://bbc.in/16dClPF', u'http://www.bbc.co.uk/sport/0/21711199#TWEET650562'], u'http://bbc.in/16dClPF': [u'http://bbc.in/16dClPF', u'http://www.bbc.co.uk/sport/0/21711199#TWEET650562']}
 >>> # note that bad shortlink URLs have a key to an empty list (lost/forgotten shortlink URLs don't generate any error)
```


changelog
---------

* 2019/02/17 1.1.1 Minor release to fix Python 3 support for utils.py, test with 3.7
* 2015/04/11 1.1.0 Add basic support for Python 3
* 2014/07/30 1.0.3 Update parsed URLs for Twitter API 1.1 compatibility
* 2013/06/01 1.0.1 new working version, adding comma parse fix (thanks https://github.com/muckrack), used autopep8 to clean the src, added a shortlink expander
* 2013/02/11 1.0.0.2 released to PyPI


tests
-----

Run the unit tests:

    $ python ttp/tests.py
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
page](https://github.com/edmondburnett/twitter-text-python/wiki/Contributing) for
notes on contributing to **twitter-text-python**.


history
-------

The current version was forked by Edmond Burnett in July 2014:
https://github.com/edmondburnett/twitter-text-python

The library was forked by Ian Ozsvald in January 2013 and released to PyPI,
some bugs were fixed, a few minor changes to functionality added (no longer
supported): https://github.com/ianozsvald/twitter-text-python

The original ttp comes from Ivo Wetzel (no longer supported):
https://github.com/BonsaiDen/twitter-text-python

Originally based on
[https://github.com/mzsanford/twitter-text-java](https://github.com/mzsanford/twitter-text-java).
