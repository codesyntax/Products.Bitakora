README.txt

  Copy this folder in your $INSTANCE_HOME/Products folder, install the products indicated by DEPENDENCIES.txt file and restart Zope.

You will have two extra products:

 - Squishblog: Fully featured blog product for Zope. With ideas of Squishdot and COREBlog.
 
 - SquishblogCommunity: A way for having a blog community based on Squishblog.
 
 
Squishblog Features

 - All templates and scripts are in the File System.

 - A user with a custom role called 'Blogger' and created with the product, can manage the blog without having access to the ZMI.

 - Epoz editor integrated.

 - Fully i18n-ed using Localizer. A MessageCatalog called 'gettext' can be found in each blog with the messages to translate.

 - Full UTF-8 support, trying to avoid painfull UnicodeDecodeErrors :)

 - All posts are indexed using TextIndexNG2, for providing quick and powerfull searches across the site.

 - Blog templates are clean XHTML based on MovableType 3 templates.

 - Clean URLs and tag based categorization of posts.


SquishblogCommunity Features

 - All template and scripts are loaded to the ZMI during instantiation of the product, in the same way Squishdot does, to allow community managers to customize it.

 - Fully i18n-ed using Localizer.

 - Free creation of blogs, in a 3-step-Blogger-way.

 - Full indexing of blog posts for providing quick and powerfull searches of the blogs using TextIndexNG2.