twitter-text-python
===================

**twitter-text-python** is a Tweet parser and formatter for Python. Extract users, hashtags, URLs and format as HTML for display.

It is based on twitter-text-java_ and passes all the unittests of 
twitter-text-conformance_ plus some additional ones.

.. _twitter-text-java: http://github.com/mzsanford/twitter-text-java
.. _twitter-text-conformance: http://github.com/mzsanford/twitter-text-conformance

This version was forked by Ian Ozsvald in January 2013 and released to PyPI, some bugs were fixed, a few minor changes to functionality added:
https://github.com/ianozsvald/twitter-text-python

PyPI release:
http://pypi.python.org/pypi/twitter-text-python/

The original ttp comes from Ivo Wetzel (Ivo's version no longer supported):
https://github.com/BonsaiDen/twitter-text-python

Usage::

    >>> import ttp
    >>> p = ttp.Parser()
    >>> result = p.parse("@ianozsvald, you now support #IvoWertzel's tweet parser! https://github.com/ianozsvald/")
    >>> result.reply
    'ianozsvald'
    >>> result.users
    ['ianozsvald']
    >>> result.tags
    ['IvoWertzel']
    >>> result.urls
    ['https://github.com/ianozsvald/']
    >>> result.html
    u'<a href="http://twitter.com/ianozsvald">@ianozsvald</a>, you now support <a href="http://search.twitter.com/search?q=%23IvoWertzel">#IvoWertzel</a>\'s tweet parser! <a href="https://github.com/ianozsvald/">https://github.com/ianozsvald/</a>'

