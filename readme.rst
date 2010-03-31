twp - TWitter(Text)Python
=========================

**twp** is a Tweet parser and formatter for Python.

It is based on the Java Implementation_ of the Twitter Text Library.
The unittests are nearly a exact copy of the ones for the Java Library_.

.. _Implementation: http://github.com/mzsanford/twitter-text-java
.. _Library: http://github.com/mzsanford/twitter-text-conformance/blob/master/autolink.yml
.. _Atarashii: http://github.com/BonsaiDen/Atarashii/

Usage::

    >>> import twp
    >>> f = twp.Formatter()
    >>> result = f.format("@BonsaiDen Hey that's a great Tweet Parser! #twp")
    >>> result
    <twp.FormatResult instance at 0xb77d9aec>
    >>> result.html
    u'<a href="http://twitter.com/BonsaiDen">@BonsaiDen</a> Hey that\'s a great Tweet Parser! 
    <a href="http://search.twitter.com/search?q=%23AtarashiiFormat">#twp</a>'
    >>> result.tags
    ['twp']
    >>> result.users
    ['BonsaiDen']
    >>> result.urls
    []


If you need different HTML output just subclass and override the ``format_*`` methods.


Todo
----

- Add support for lists.


Contributing
------------

The source is available on GitHub_, to
contribute to the project, fork it on GitHub and send a pull request.
Everyone is welcome to make improvements to **twp**!

.. _GitHub: http://github.com/BonsaiDen/twp

License
=======

Copyright (c) 2010 Ivo Wetzel

**twp** is free software: you can redistribute it and/or 
modify it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

**twp** is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
**twp**. If not, see <http://www.gnu.org/licenses/>.

