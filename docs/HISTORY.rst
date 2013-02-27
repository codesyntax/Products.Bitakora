===========
CHANGELOG
===========

1.0.1 (2013/02/27)
====================

- Documentation improvement [erral]

1.0 (2013/02/22)
==================

- Remove TextIndexNG2 dependency and provide migration to delete indexes [erral]

- PEP8ify [erral]

- Provide migration for old instances [erral]

- Fix attribute name clash issue [erral]

- Reformat README and HISTORY files in rST [erral]

- Add TinyMCE insted of epoz [erral

- Eggify this product [erral]


v. 0.1.21
==========
- Fix e-mail templates [erral]


v. 0.1.20
==========
- Change CAPTCHA using a question. [erral]

v. 0.1.19
==========

- Re-add HTML parsing for comments to avoid arbitrary JavaScript
  to be added in the comments. Thanks to Iker Mendilibar. [erral]

v. 0.1.16
=========
- Use string interpolation in community templates

- Add error control when an user asks password reminder twice.


v. 0.1.15
==========
- Modified the way to handle pings. Now the pings are handled making Future calls,
  creating new threads to make the pings

v. 0.1.10
=========
- Fixed bug, when creating comment ids


v. 0.1.9
========
- Allow more attributes in HTML

v. 0.1.8
========
- CAPTCHA control is enabled by defatul. To disable add a property called
  CAPTCHA_ENABLED and set it to 0 (property type: int)

- Akismet plugin is disabled by default. To enable change utils.py

- Added Akismet spam control for comments and pingbacks

- Added CAPTCHA control to comment adding and contact form. Captcha images
  and example code provided by http://www.captchas.net

- Fixed: contact and new comments notifications are properly i18n-zed

- Ping to Technorati added

- Fixed: Ping to Technorati and Ping-o-matic. The ping must be sent with blog
  title and not with post title

v. 0.1.7
========
- Fixed bug in post edit form. If a method called 'preview' existed, it was not
  posible to edit a post.

v. 0.1.6
========
- New Polish translation
- Pingback system re-enabled and fixed

v. 0.1.5
========
- 'u' and 'del' tags allowed in HTML
- Changed community CSS file images, now they are GIF instead of JPEG


v. 0.1.4
========
- Deleted email from feed.xml. RSS 2.0 says author tag must contain an email address.
  Added DC namespace to the feed and exchanged author with dc:creator

- Allow embed, object and param tags in HTML for inserting YouTube and GoogleVideo flashes

- Allow '-' and '_' in tags

- Show cleaned HTML in post preview

- Changes to show the tag cloud

- Fixed password reminder in community


v. 0.1.3 (first version for Blogak.com)
=======================================

- Fixed bug in XML exporting

- Added contact form

- Add, blog author receives an email when a post is commented

- Modify, Pingomatic ping re-enabled, and pingback send disabled

- Updated eu and es translations

- Minor changes in admin screens


v. 0.1.2 (not public, for testing at atxukale.com)
==================================================

- Some methods refactored

- Bug: Recent comments menu showed all comments, now is limited to 10

- Bug: Comment author's e-mail was shown.

- Add, now it's possible to export a XML file with blog data

- Change, CSS styles both in community and blogs fixed for IE


v. 0.1.1 (not public, for testing at atxukale.com)
==================================================

- Add, posibility to import XML file with blog data

- Add, parameter to signal wether pinging and HTML cleaning is wanted: pinging disabled by default and HTML cleaning enabled

- Changed, Pingback disabled when adding posts


v. 0.1 - Initial Release
========================

- Initial release [erral]