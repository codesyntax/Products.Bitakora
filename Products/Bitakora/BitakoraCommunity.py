# -*- coding: utf-8 -*-
# (c) Copyright 2005, CodeSyntax <http://www.codesyntax.com>
# Authors: Mikel Larreategi <mlarreategi@codesyntax.com>
# See also LICENSE.txt

""" Bitakora community """

# Zope modules
from AccessControl import ClassSecurityInfo
import Globals
from Globals import HTMLFile

# Modules from Localizer
from Products.Localizer.Localizer import Localizer
from Products.Localizer.MessageCatalog import MessageCatalog
from Products.Localizer.LocalContent import LocalContent

# ZCatalog
from Products.ZCatalog import ZCatalog

# CookieCrumbler
try:
    from Products.CookieCrumbler.CookieCrumbler import CookieCrumbler
except:
    from Products.CMFCore.CookieCrumbler import CookieCrumbler

# BTreeFolder2
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2

from utils import addDTML, addPythonScript, addImage
from utils import addFile, fillMessageCatalog
import DateTime

try:
    True
except:
    True = 1
    False = 0

manage_addBitakoraCommunityForm = HTMLFile('ui/BitakoraCommunity_add',
                                            globals())


def manage_addBitakoraCommunity(self, id, admin_mail, REQUEST=None):
    """ add Bitakora Community """
    self._setObject(id, BitakoraCommunity(id, admin_mail))
    com = getattr(self, id)
    com.Catalog.refreshCatalog(1)

    if REQUEST is not None:
        return self.manage_main(self, REQUEST)


class BitakoraCommunity(BTreeFolder2):
    """ BTreeFolder2 container for Bitakora community.
        It will contain blogs and methods for the main page of the community
    """
    meta_type = 'BitakoraCommunity'

    security = ClassSecurityInfo()
    security.setPermissionDefault('Manage BitakoraCommunity', ('Manager', ))

    _properties = ({'id': 'admin_mail', 'type': 'ustring', 'mode': 'w'},
                   {'id': 'management_page_charset',
                    'type': 'string',
                    'mode': 'w'},
                   {'id': 'title', 'type': 'ustring', 'mode': 'w'})

    manage_adminBlogs = HTMLFile('ui/admin_blogs', globals())
    manage_adminUsers = HTMLFile('ui/admin_users', globals())

    def __init__(self, id, admin_mail):
        """ Create Bitakora community """
        BTreeFolder2.__init__(self, id)
        self.id = id
        self.admin_mail = admin_mail
        self.management_page_charset = 'UTF-8'
        self.title = u'blog community'
        self._addLocalizer()
        self._addCatalog()
        self._addMethods()
        self._addTemplates()
        self._addContent()
        self._addOthers()
        self._buildIndexes()

    def _addLocalizer(self):
        """ Add Localizer stuff """
        try:
            # old MessageCatalog
            self._setObject('gettext',
                            MessageCatalog('gettext', '', ('en', 'eu', 'es')))
        except:
            # new MessageCatalog
            self._setObject('gettext',
                    MessageCatalog('gettext', '', 'en', ['en', 'eu', 'es']))

        # fill the gettext with 'es' and 'eu' locales
        gettext = getattr(self, 'gettext')
        fillMessageCatalog(gettext)
        localizer = Localizer('Localizer', ('en',))
        localizer._v_hook = 1
        self._setObject('Localizer', localizer)

    def manage_options(self):
        """ """
        options = (BTreeFolder2.manage_options[0],) \
                 + ({'label': ('Admin'),
                    'action': 'manage_adminBlogs'},
                    {'label': ('Users'),
                    'action': 'manage_adminUsers'}) \
                 + BTreeFolder2.manage_options[1:]

        return options

    def _addOthers(self):
        """ Add other stuff """
        self.manage_addUserFolder()
        self._setObject('cookie_authentication',
                        CookieCrumbler('cookie_authentication'))

    def _addCatalog(self):
        """ Add ZCatalog instance """
        self._setObject('Catalog', ZCatalog.ZCatalog('Catalog', 'Catalog'))

    def _buildIndexes(self):
        """ Stuff to create Catalog indexes """
        # get the Catalog in a BTreeFolder2 way: as if it was a dictionary
        catalog = self.get('Catalog')
        # delete any existing indexes
        for name in catalog.indexes():
            catalog.delIndex(name)

        # add the default indexes
        for (name, index_type) in [('meta_type', 'FieldIndex'),
                                  ('published', 'FieldIndex'),
                                  ('date', 'DateIndex'),
                                  ('tags', 'KeywordIndex'),
                                  ('yearmonth', 'KeywordIndex'),
                                  ('postcount', 'FieldIndex'),
                                  ('users', 'FieldIndex')]:
            catalog.addIndex(name, index_type)

        # delete the default metadata columns
        for name in catalog.schema():
            catalog.delColumn(name)

    def _addMethods(self):
        """ method for adding templates, scripts, ... """

        dtmls = ['blogs_main', 'column', 'create_blog_form',
                 'index_html', 'last_posts']
        dtmls.extend(['logged_in', 'logged_out', 'login_form',
                      'entry_body_community'])
        dtmls.extend(['menu', 'mini_login_form', 'preheader',
                      'default_template'])
        dtmls.extend(['standard_html_footer', 'standard_html_header',
                      'step1', 'step2', 'step3'])
        dtmls.extend(['step3.done', 'tag_all_html', 'tag_html'])
        dtmls.extend(['reminder', 'reminder.done', 'changepass'])
        for dtml in dtmls:
            addDTML(self, dtml, '', 'ui/communityTemplates/%s' % dtml)

        scripts = ['step1.do', 'step2.do', 'step3.do', 'tag',
                   'tagsAndPixels', 'usersBlog', 'logout']
        scripts.extend(['reminder.do', 'changepass.do'])
        for script in scripts:
            addPythonScript(self, script, 'ui/communityTemplates/%s' % script)
            ob = getattr(self, script)
            ob._proxy_roles = ('Manager',)

    def _addTemplates(self):
        """ add some CSS and images """
        self.manage_addFolder('img')
        self.manage_addFolder('templates')
        import os
        file_path = Globals.package_home(globals())
        # just files
        all = os.listdir(file_path + '/ui/communityTemplates')

        imgs = [f for f in all if f.endswith('jpg') or f.endswith('gif')]
        for img in imgs:
            addImage(self.img, img, 'ui/communityTemplates/%s' % img)

        files = [f for f in all if f.endswith('css')]
        for file in files:
            addFile(self.img, file, 'ui/communityTemplates/%s' % file)

        for num in range(1, 5):
            self.templates.manage_addFolder('%s' % num)
            fol = getattr(self.templates, '%s' % num)
            addFile(fol, 'blog.css', 'ui/communityTemplates/%s/blog.css' % num)

    def _addContent(self):
        """ add some LocalContents for fixed content """
        languages = 'en'
        contents = ['about', 'us', 'contents']
        for content in contents:
            try:
                #old LocalContent
                self._setObject(content,
                                LocalContent(content, tuple(languages)))
            except:
                # new LocalContent
                self._setObject(content,
                                LocalContent(content, 'en', tuple(languages)))

    security.declareProtected('Manage BitakoraCommunity', 'delBlogs')

    def delBlogs(self, ids=[], REQUEST=None):
        """ delete selected blogs """
        del_users = []

        for id in ids:
            blog = self.get(id)
            rol = blog.get_local_roles()
            del_users.extend([user for user, roles in rol])
            blog_path = '/'.join(blog.getPhysicalPath())
            self.Catalog.uncatalog_object(blog_path)
            for post in blog.published_posts(size=99999):
                self.Catalog.uncatalog_object(post.getPath())

        self.manage_delObjects(ids)
        self.delUsers(del_users)

        if REQUEST is not None:
            url = REQUEST.HTTP_REFERER.split('?')[0]
            return REQUEST.RESPONSE.redirect(url + '?msg=%s' % 'Blogs deleted successfully')

    security.declareProtected('Manage BitakoraCommunity', 'delUsers')

    def delUsers(self, ids=[], REQUEST=None):
        """ delete selected blogs """

        self.acl_users.userFolderDelUsers(ids)

        if REQUEST is not None:
            url = REQUEST.HTTP_REFERER.split('?')[0]
            return REQUEST.RESPONSE.redirect(url+'?msg=%s' % 'Users deleted successfully')

    security.declarePublic('cleanHTML')

    def cleanHTML(self, html):
        """ clean html from posts """
        # Which one is more efficient?
        # One way...
        try:
            from EpozPostTidy import cleanHTML as clean
            return clean(html)
        except:
            # perhaps more efficient but needed for old Zopes
            # Another way... (from Zopelabs)
            intag = [False]

            def chk(c, intag):
                if intag[0]:
                    intag[0] = (c != '>')
                    return False
                elif c == '<':
                    intag[0] = True
                    return False
                return True

            return ''.join([c for c in html if chk(c, intag)])

    security.declarePublic('community')

    def community(self):
        """ return the community """
        return self

    security.declarePublic('communityTitle')

    def communityTitle(self):
        """ return the title """
        return self.title

    security.declarePublic('communityUrl')

    def communityUrl(self):
        """ return the URL of the community """
        return self.absolute_url()

    security.declarePublic('communityLastPosts')

    def communityLastPosts(self, size=10, start=None):
        """ The method for getting 'size' published posts"""
        if start is None:
            return self.Catalog.searchResults(meta_type='Post',
                                              published=1,
                                              sort_limit=size,
                                          date={'query': DateTime.DateTime(),
                                                'range': 'max'},
                                              sort_on='date',
                                              sort_order='descending')
        else:
            return self.Catalog.searchResults(meta_type='Post',
                                              published=1,
                                          date={'query': DateTime.DateTime(),
                                                'range': 'max'},
                                              sort_on='date',
                                              sort_order='descending')

    security.declareProtected('Manage Bitakora', 'migrate_textindexng2')

    def migrate_textindexng2(self):
        """ remove all textindeng2 indexes """
        from logging import getLogger
        log = getLogger('migrate_textindexng2')
        indexes = ['author', 'body', 'excerpt', 'title']
        for index in indexes:
            if index in self.Catalog.indexes():
                self.Catalog.manage_delIndex(index)
                log.info('Deleted %s index' % index)
        log.info('Deleted TextIndexNG2 indexes')

    security.declareProtected('Manage Bitakora', 'migrate_to_1_dot_0')

    def migrate_to_1_dot_0(self):
        """ migrate to Bitakora 1.0 """
        import transaction
        from logging import getLogger
        log = getLogger('migrate_to_1_dot_0')
        self.migrate_textindexng2()
        for blog in self.objectValues('Bitakora'):
            log.info('Migrating: %s' % blog.getId())
            blog.migrate_to_1_dot_0()
            transaction.savepoint(optimistic=True)

        log.info('done')

Globals.InitializeClass(BitakoraCommunity)
