=============
Bitakora
=============

  Copy this folder in your $INSTANCE_HOME/Products folder, install the products indicated by DEPENDENCIES.txt file and restart Zope.

You will have two extra products to add in the ZMI:

 - Bitakora: Fully featured blog product for Zope. With ideas of Squishdot and COREBlog.

 - BitakoraCommunity: A way for having a blog community based on Bitakora product.


Bitakora Features
========================

 - All templates and scripts are in the File System.

 - A user with a custom role called 'Blogger' and created with the product, can manage the blog without having access to the ZMI.

 - Epoz editor integrated.

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

 - Full indexing of blog posts for providing quick and powerfull searches on the blogs using TextIndexNG2.

More info
===============

 - `Bitakora blog community`_

 - `Bitakora mailing list`_

 - `Blogak.com`_


Migration to 1.0
====================

 - To migrate from 0.x version to 1.0, open http://yoursite.com/blog/migrate_to_1_dot_0 or
   http://yoursite.com/community/migrate_to_1_dot_0 to run migration code. This migration
   code, adds TinyMCE, fixes attribute name clash in Comment class and deletes TextIndexNG2
   indexes created in the installtion

License
=========

See LICENSE.txt


.. _`Pingback references`: http://www.hixie.ch/specs/pingback/pingback
.. _`Pingomatic`: http://pingomatic.com
.. _`Bitakora blog community`: http://www.codesyntax.com/bitakora
.. _`Bitakora mailing list`: http://groups.yahoo.com/group/bitakora
.. _`Blogak.com`: http://www.blogak.com
