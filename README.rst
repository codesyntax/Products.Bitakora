=============
Bitakora
=============

Bitakora is a fully featured Blog product for Zope. Yes plain Zope, nor Plone neither CMF is involved.

You will have two extra products to add in the ZMI:

- Bitakora: Fully featured blog product for Zope. With ideas of Squishdot and COREBlog.

- BitakoraCommunity: A way for having a blog community based on Bitakora product.


Bitakora Features
========================

- All templates and scripts are in the File System.

- A user with a custom role called 'Blogger' and created with the product, can manage the blog without having access to the ZMI.

- TinyMCE as WYSIWYG editor..

- Fully i18n-ed using Localizer. A MessageCatalog called 'gettext' can be found in each blog with the messages to translate. Basque (eu) and Spanish (es) translations are provided with the product (see locale directory). This MessageCatalog is deleted when creating blogs in a BitakoraCommunity, and blogs use the MessageCatalog in the community.

- Full UTF-8 support, trying to avoid UnicodeDecodeErrors :)

- Blog templates are clean XHTML, based on MovableType 3 templates.

- Clean URLs and tag based categorization of posts.

- Support of `Pingback references`_

- Automatic update ping to Pingomatic_


BitakoraCommunity Features
===========================

- All template and scripts are loaded into the ZMI during instantiation of the product, in the same way Squishdot does, to allow community managers to customize them.

- Free creation of blogs, in a 3-step-Blogger-way.

- Fully i18n-ed using Localizer. Basque (eu) and Spanish (es) translations are provided with the products (see locale directory).


Installation
================

We suggest using `zc.buildout`_ to handle the installation of Bitakora. For that purpose
we provide a buildout file to use as an example:

https://github.com/codesyntax/Products.Bitakora/blob/master/example-buildout.cfg


If you plan to install manually, you should install these products:

- Zope 2.11 (we use the latest 2.11 release: 2.11.8)

- itools 0.20.8 (you need to install glib development headers to correctly install
  itools in Ubuntu/Debian system you need to `apt-get install libglib2-dev`)

- Localizer 1.2.3

- CookieCrumbler 1.2

- ZTinyMCE 0.2.1 (the original website for ZTinyMCE is down, so we have uploaded
  this product `to our GitHub account`_, just for the purpose of have this buildout
  working)


Migration to 1.0
====================

To migrate from 0.x version to 1.0, open http://yoursite.com/blog/migrate_to_1_dot_0 or
http://yoursite.com/community/migrate_to_1_dot_0 to run migration code. This migration
code, adds TinyMCE, fixes attribute name clash in Comment class and deletes TextIndexNG2
indexes created in the installtion


More info
===============

- `Bitakora blog community`_

- `Bitakora mailing list`_

- `Blogak.com`_


Thanks
=============

The development of this product was partialy funded by `Gipuzkoako Foru Aldundia`_
(Gipuzkoan Foral Government) and `Eusko Jaurlaritza`_ (Basque Regional Government).


License
=========

BSD Like. See `LICENSE.txt`


.. _`Gipuzkoako Foru Aldundia`: http://www.gipuzkoaeuskara.net
.. _`Eusko Jaurlaritza`: http://www.euskadi.net
.. _`Pingback references`: http://www.hixie.ch/specs/pingback/pingback
.. _`Pingomatic`: http://pingomatic.com
.. _`Bitakora blog community`: http://www.codesyntax.com/bitakora
.. _`Bitakora mailing list`: http://groups.yahoo.com/group/bitakora
.. _`Blogak.com`: http://www.blogak.com
.. _`LICENSE.txt`: https://github.com/codesyntax/Products.Bitakora/blob/master/docs/LICENSE.txt
.. _`zc.buildout`: http://www.buildout.org
.. _`to our GitHub account`: http://github.com/codesyntax/ZTinyMCE/archive/0.2.1.tar.gz

