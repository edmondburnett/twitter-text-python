twitter-text-python
===================

**twitter-text-python** is a Tweet parser and formatter for Python.

It is based on twitter-text-java_ and passes all the unittests of 
twitter-text-conformance_ plus some additional ones.

.. _twitter-text-java: http://github.com/mzsanford/twitter-text-java
.. _twitter-text-conformance: http://github.com/mzsanford/twitter-text-conformance/blob/master/autolink.yml

Usage::

    >>> import ttp
    >>> p = ttp.Parser()
    >>> result = p.parse("@BonsaiDen Hey that's a great Tweet parser! #twp")
    >>> result.reply
    'BonsaiDen'
    >>> result.users
    ['BonsaiDen']
    >>> result.tags
    ['twp']
    >>> result.urls
    []
    >>> result.html
    u'<a href="http://twitter.com/BonsaiDen">@BonsaiDen</a> Hey that\'s a great Tweet Parser! 
    <a href="http://search.twitter.com/search?q=%23twp">#twp</a>'


If you need different HTML output just subclass and override the ``format_*`` methods.


Contributing
------------

The source is available on GitHub_, to
contribute to the project, fork it on GitHub and send a pull request.
Everyone is welcome to make improvements to **twp**!

.. _GitHub: http://github.com/BonsaiDen/twitter-text-python

License
=======

Copyright (c) 2010 Ivo Wetzel

**twitter-text-python** is free software: you can redistribute it and/or 
modify it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

**twitter-text-python** is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
**twitter-text-python**. If not, see <http://www.gnu.org/licenses/>.

