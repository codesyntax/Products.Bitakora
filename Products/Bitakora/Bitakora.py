# -*- coding: utf-8 -*-
# (c) Copyright 2005, CodeSyntax <http://www.codesyntax.com>
# Authors: Mikel Larreategi <mlarreategi@codesyntax.com>
# See also LICENSE.txt

# Zope modules
from Globals import HTMLFile
import Globals
from AccessControl import ClassSecurityInfo

from BTrees.IOBTree import IOBTree
from Products.PythonScripts.PythonScript import PythonScript

# ZCatalog
from Products.ZCatalog import ZCatalog
from Products.ZCatalog.CatalogPathAwareness import CatalogAware
# Localizer
from Products.Localizer.Localizer import Localizer
from Products.Localizer.MessageCatalog import MessageCatalog
# BTreeFolder2
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2
# Other stuff
import DateTime

# Own modules
from utils import addDTML
from utils import fillMessageCatalog, ok_chars
from PingMethodContainer import PingMethodContainer
from tinymce_conf import default_configurations

manage_addBitakoraForm = HTMLFile('ui/Bitakora_add', globals())


def manage_addBitakora(self, id, title, subtitle,
                       contact_mail, description=u'', REQUEST=None):
    """ Method called from ZMI to create a new Bitakora """
    import Bitakora
    sq = Bitakora.Bitakora(id, title, subtitle, description, contact_mail)
    self._setObject(id, sq)
    sq = getattr(self, id)

    if REQUEST is not None and REQUEST.get('image', None):
        image = REQUEST.get('image')
        ext = image.filename.split('.')[-1]
        imgid = 'image.%s' % ext
        sq.manage_addImage(imgid, REQUEST.get('image'))
        #sq.imageUrl = '%s/%s' % (sq.absolute_url(), imgid)
        sq.imagename = imgid

    elif REQUEST is None or not REQUEST.get('image', None):
        from random import random

        imgnum = (int(random() * 10) % 3) + 1
        file = 'face0%s.gif' % imgnum
        file_path = Globals.package_home(globals())
        f = open(file_path + '/ui/communityTemplates/' + file, 'rb')
        contents = f.read()
        f.close()
        title = ''
        imgid = 'image.gif'
        sq.manage_addImage(imgid, contents, title=title)
        sq.imagename = imgid

    perms = {}
    perms['Anonymous'] = ['Add Bitakora Comment']
    perms['Blogger'] = ['Manage Bitakora']

    for role, perm in perms.items():
        sq.manage_role(role_to_manage=role, permissions=perm)

    sq.manage_addProduct['ZTinyMCE'].manage_addZTinyMCE('TinyMCE', 'TinyMCE')
    maker = sq.manage_addProduct['ZTinyMCE'].manage_addZTinyConfiguration
    for config in default_configurations:
        maker(config['name'], configuration=config['config'],
              tinymce_instance_path='/'.join(sq.TinyMCE.getPhysicalPath()),
              title='Example configuration',
              optimize=True)

    # Add a MessageCatalog if we are a standalone Bitakora
    # if not, the BitakoraCommunity MessageCatalog will handle
    # the messages
    if self.meta_type == 'BitakoraCommunity':
        sq._delObject('Localizer')
        sq._delObject('gettext')
        self.Catalog.catalog_object(sq, '/'.join(sq.getPhysicalPath()))

    if REQUEST is not None:
        return self.manage_main(self, REQUEST)


class Bitakora(BTreeFolder2, CatalogAware):
    """ Bitakora is a new blog product for Zope """
    from Post import manage_addPost
    from utils import send_contact_mail, cleanBody, getCaptchaQuestion

    meta_type = 'Bitakora'

    __ac_roles__ = ('Blogger',)

    security = ClassSecurityInfo()
    security.setDefaultAccess('allow')

    security.setPermissionDefault('Manage Bitakora', ('Blogger', 'Manager',))
    security.setPermissionDefault('Add Bitakora Comment',
                                  ('Anonymous', 'Manager',))

    _properties = (
                   {'id': 'management_page_charset',
                    'type': 'string',
                    'mode': 'w'},
                   {'id': 'CAPTCHA_ENABLED',
                    'type': 'int'},
                   )

    manage_options = ({'label': 'Contents', 'action': 'manage_main'},
                      {'label': 'View', 'action': 'index_html'},
                      {'label': 'Security', 'action': 'manage_access'},
                      {'label': 'Undo', 'action': 'manage_UndoForm'},)

    contact = HTMLFile('ui/contact', globals())
    archive = HTMLFile('ui/archive', globals())
    captcha_control = HTMLFile('ui/captcha_control', globals())
    comment_body = HTMLFile('ui/comment_body', globals())
    comment_email_template = HTMLFile('ui/comment_email_template', globals())
    comment_form = HTMLFile('ui/comment_form', globals())
    contact_email_template = HTMLFile('ui/contact_email_template', globals())
    entry_body = HTMLFile('ui/entry_body', globals())
    entry_preview = HTMLFile('ui/entry_preview', globals())
    index_html = HTMLFile('ui/index_html', globals())
    localmenu = HTMLFile('ui/localmenu', globals())
    admin_header = HTMLFile('ui/admin_header', globals())
    about = HTMLFile('ui/about', globals())
    contents = HTMLFile('ui/contents', globals())
    downloadTXT = HTMLFile('ui/downloadTXT', globals())
    downloadXML = HTMLFile('ui/downloadXML', globals())
    downloadWordPress = HTMLFile('ui/downloadWordPress', globals())
    logged_in = HTMLFile('ui/logged_in', globals())
    logged_out = HTMLFile('ui/logged_out', globals())
    login_form = HTMLFile('ui/login_form', globals())
    posting_html = HTMLFile('ui/posting_html', globals())
    recent_comments = HTMLFile('ui/recent_comments', globals())
    recent_references = HTMLFile('ui/recent_references', globals())
    reference_body = HTMLFile('ui/reference_body', globals())
    #standard_error_message = HTMLFile('ui/standard_error_message', globals())
    standard_html_footer = HTMLFile('ui/standard_html_footer', globals())
    standard_html_header = HTMLFile('ui/standard_html_header', globals())
    tag_all_html = HTMLFile('ui/tag_all_html', globals())
    tag_html = HTMLFile('ui/tag_html', globals())
    user_links = HTMLFile('ui/user_links', globals())

    security.declareProtected('Manage Bitakora', 'manage_addPost')

    security.declareProtected('Manage Bitakora', 'admin')
    admin = HTMLFile('ui/Post_list', globals())

    security.declareProtected('Manage Bitakora', 'post')
    post = HTMLFile('ui/Post_add', globals())

    security.declareProtected('Manage Bitakora', 'prefs')
    prefs = HTMLFile('ui/Blog_edit', globals())

    security.declareProtected('Manage Bitakora', 'sidebar')
    sidebar = HTMLFile('ui/manage_sidebar', globals())

    security.declareProtected('Manage Bitakora', 'template')
    template = HTMLFile('ui/manage_template', globals())

    security.declareProtected('Manage Bitakora', 'comments')
    comments = HTMLFile('ui/manage_comments', globals())

    admin_options = ['admin', 'post', 'sidebar',
                     'prefs', 'template', 'comments']

    security.declarePrivate('__init__')

    def __init__(self, id, title, subtitle, description, contact_mail):
        """ Constructor """
        BTreeFolder2.__init__(self, id)
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.contact_mail = contact_mail
        self.management_page_charset = u'UTF-8'
        self.sidebar_html = u''
        self._setObject('Catalog', ZCatalog.ZCatalog('Catalog', 'Catalog'))
        self._buildIndexes()
        self._addMethods()
        self._setObject('pingback', PingMethodContainer())
        self.postcount = 0
        self._links = IOBTree()
        # if 0 not allowed, 1 allowed, 2 allowed but moderated
        self.comment_allowed = 1
        self.reference_allowed = 1
        #self.imageUrl = None
        self.imagename = ''
        self.CAPTCHA_ENABLED = 1

    security.declareProtected('View', 'searchResults')

    def searchResults(self, **kw):
        """ Call the Catalog """
        return self.Catalog.searchResults(kw)

    security.declareProtected('View', 'all')

    def all(self, REQUEST=None, **kw):
        """ Just a wrapper around call """
        return self.Catalog(REQUEST, **kw)

    security.declareProtected('Manage Bitakora', 'editBlog')

    def editBlog(self, title, subtitle, contact_mail,
                 description, image=None, REQUEST=None):
        """ editing method """
        self.title = title
        self.subtitle = subtitle
        self.contact_mail = contact_mail
        self.description = description
        if image.read():
            if not image.headers['Content-Type'].lower().startswith('image'):
                return REQUEST.RESPONSE.redirect('%s/prefs?msg=%s' %
                            (self.blogurl(),
                            'You tried to upload something that is not a valid picture image. Try with a 65x65 pixel sized jpg, png or gif.'))

            ext = image.filename.split('.')[-1]
            imgid = 'image.%s' % ext
            #original_id = self.imageUrl.split('/')[-1]
            original_id = self.imagename
            original_img = self.get(original_id).data
            self._delObject(original_id)

            image.seek(0)
            self.manage_addImage(imgid, image)

            img = self.get(imgid)
            if img.height > 65 and img.width > 65:
                self._delObject(imgid)
                self.manage_addImage(original_id, original_img)
                #self.imageUrl = '%s/%s' % (self.absolute_url(), original_id)
                self.imagename = original_id
                if REQUEST is not None:
                    return REQUEST.RESPONSE.redirect('%s/prefs?msg=%s' % (self.blogurl(), 'Your image is too large. Try with a smaller one'))

            #self.imageUrl = '%s/%s' % (self.absolute_url(), imgid)
            self.imagename = imgid

        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('%s/prefs?msg=%s' % (self.blogurl(),
                                            'Preferences edited succesfully'))

    security.declareProtected('Manage Bitakora', 'editCommentPolicy')

    def editCommentPolicy(self, comment_allowed, REQUEST=None):
        """ edit comment policy """
        self.comment_allowed = comment_allowed
        self.reference_allowed = comment_allowed

        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('%s/comments?msg=%s' % (self.blogurl(), 'Comment policy edited succesfully'))

    security.declarePrivate('_buildIndexes')

    def _buildIndexes(self):
        """ Stuff to create Catalog indexes """
        # delete any existing indexes
        for name in self.Catalog.indexes():
            self.Catalog.delIndex(name)

        # add the default indexes
        for (name, index_type) in [('meta_type', 'FieldIndex'),
                                   ('published', 'FieldIndex'),
                                   ('date', 'DateIndex'),
                                   ('tags', 'KeywordIndex'),
                                   ('yearmonth', 'KeywordIndex')]:
            self.Catalog.addIndex(name, index_type)

    security.declarePrivate('_addMethods')

    def _addMethods(self):
        """ Just to have all methods adding something extra
            to the ZMI together """
        file_path = Globals.package_home(globals())

        localizer = Localizer('Localizer', ('en', 'es', 'eu',))
        localizer._v_hook = 1
        self._setObject('Localizer', localizer)

        try:
            # old MessageCatalog
            self._setObject('gettext',
                    MessageCatalog('gettext', '', ('en', 'es', 'eu')))
        except:
            # new MessageCatalog
            self._setObject('gettext',
                    MessageCatalog('gettext', '', 'en', ['en', 'es', 'eu']))

        gettext = getattr(self, 'gettext')
        fillMessageCatalog(gettext)

        # Add a special tag.py script which makes use of traverse subpath
        self._setObject('tag', PythonScript('tag'))
        tag = getattr(self, 'tag')
        f = open(file_path + '/tag.py')
        data = f.read()
        f.close()
        tag.ZPythonScript_edit('', data)

        # Add a feed.xml file with the RSS feed
        addDTML(self, 'feed.xml', '', 'ui/feed.xml')

        # Add the CSS file
        self.manage_addFile('blog.css')
        css = getattr(self, 'blog.css')
        f = open(file_path + '/ui/blog.css')
        data = f.read()
        f.close()
        css.update_data(data)

    security.declareProtected('Manage Bitakora', 'manage_delPosts')

    def manage_delPosts(self, ids=[], REQUEST=None):
        """ To delete posts from ZMI """
        for id in ids:
            obj = getattr(self, id)
            obj.deleteAllComments()
            obj.deleteAllReferences()
            if self.inCommunity():
                # We are in a Bitakora Community, so uncatalog the post there
                cat = self.getParentNode().get('Catalog', 'None')
                if cat is not None:
                    cat.uncatalog_object('/'.join(obj.getPhysicalPath()))
            self._delObject(id)

        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('%s/admin?msg=%s' % (self.absolute_url(), 'Post deleted succesfully'))

        return self.manage_main(self, REQUEST)

    security.declareProtected('View', 'published_posts')

    def published_posts(self, size=10, start=None):
        """ The method for getting 'size' published posts"""
        if start is None:
            return self.Catalog.searchResults(meta_type='Post',
                                              published=1,
                                              date={'query': DateTime.DateTime(),
                                                    'range':'max'},
                                              sort_on='date',
                                              sort_order='descending',
                                              sort_limit=size)
        else:
            return self.Catalog.searchResults(meta_type='Post',
                                              published=1,
                                              date={'query': DateTime.DateTime(),
                                                    'range':'max'},
                                              sort_on='date',
                                              sort_order='descending')

    security.declarePublic('last_post')

    def last_post(self):
        """ return the last published post """
        posts = self.Catalog.searchResults(meta_type='Post',
                                           size=1,
                                           sort_on='date',
                                           sort_order='descending')
        if posts:
            return posts[0].getObject()

        return None

    security.declarePublic('View', 'getId')

    def getId(self):
        """ get id """
        return self.id

    security.declarePublic('blog_title')

    def blog_title(self):
        """ blog title """
        return self.title

    security.declarePublic('blog_subtitle')

    def blog_subtitle(self):
        """ blog subtitle """
        return self.subtitle

    security.declarePublic('showDescription')

    def showDescription(self):
        return self.description

    security.declarePublic('show_contact_mail')

    def show_contact_mail(self):
        """ blog contact_mail """
        return self.contact_mail

    security.declarePublic('show_sidebar_html')

    def show_sidebar_html(self):
        """ blog show_sidebar_html """
        return self.sidebar_html

    security.declarePublic('title_or_id')

    def title_or_id(self):
        """ title or id """
        return self.blog_title() or self.id

    security.declarePublic('blogurl')

    def blogurl(self):
        """ blog url """
        return self.absolute_url()

    security.declarePublic('getImageUrl')

    def getImageUrl(self):
        """ return image's url """
        try:
            self.imagename
        except:
            # For backwards compatibility :
            # image url wasn't created dinamically, but statically when saving
            # and if blog changed the url, the image wasn't shown.
            imgid = self.imageUrl.split('/')[-1]
            if self.get(imgid, None):
                self.imagename = imgid
            else:
                # Ups, something else happened here...
                imgs = [img for img in self.objectIds() if img.startswith('image')]
                if len(imgs) == 1:
                    # Well done! We have an image. The images is always
                    # saved with name 'image' and the corresponding extension
                    self.imagename = imgs[0]
                else:
                    # Two images? No..... Load a new one please...
                    self.imagename = ''

        return self.blogurl() + '/'+self.imagename


    security.declarePublic('tagsAndPixels')

    def tagsAndPixels(self):
        """ returns a dictionary with (tag, pixelSize) pairs
            based on number of posts cataloged with the tags """

        tags = [tag for tag in self.Catalog.uniqueValuesFor('tags') if tag.strip()]
        zenbat = {}
        for tag in tags:
            tagkop = self.Catalog.searchResults(tags=tag,
                                                meta_type='Post',
                                                published=1,
                                                date={'query': DateTime.DateTime(),
                                                      'range': 'max'}
                                                )
            zenbat[tag] = len(tagkop)

        maxpx = 2.30
        minpx = 0.70
        difpx = maxpx - minpx

        if zenbat.values():
            maxnum = max(zenbat.values())
            minnum = max(zenbat.values())
        else:
            maxnum = 0

        hiz = {}
        for k, v in zenbat.items():
            hiz[k] = float(difpx * v / maxnum) + minpx

        return hiz

    security.declarePrivate('blog')

    def blog(self):
        return self

    security.declareProtected('Manage Bitakora', 'addLink')

    def addLink(self, url, title, REQUEST=None):
        """ Add a new link in link menu """
        try:
            max = self._links.maxKey()
            self._links[max + 1] = (url, title)
        except ValueError:
            self._links[0] = (url, title)
        except:
            min = self._links.minKey()
            self._links[min - 1] = (url, title)
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('%s/sidebar?msg=%s' % (self.blogurl(), 'Link added succesfully'))

    security.declareProtected('Manage Bitakora', 'removeLink')

    def removeLink(self, key=None, REQUEST=None):
        """ remove link from link menu """
        if key is not None:
            try:
                del self._links[key]
            except:
                if REQUEST is not None:
                    return REQUEST.RESPONSE.redirect('%s/sidebar?msg=%s' % (self.blogurl(), 'Error when deleting selected link'))
            if REQUEST is not None:
                return REQUEST.RESPONSE.redirect('%s/sidebar?msg=%s' % (self.blogurl(), 'Selected link was removed succesfully'))
        else:
            if REQUEST is not None:
                return REQUEST.RESPONSE.redirect('%s/sidebar?msg=%s' % (self.blogurl(), 'What?'))

    security.declarePublic('showLinks')

    def showLinks(self):
        """ show links """

        def sortByKey(el1, el2):
            return cmp(el1['key'], el2['key'])

        elems = []
        for key in self._links.keys():
            url = self._links.get(key)[0]
            title = self._links.get(key)[1]
            elems.append({'url': url, 'title': title, 'key': key})

        elems.sort(sortByKey)
        return elems

    security.declareProtected('Manage Bitakora', 'save_sidebar_html')

    def save_sidebar_html(self, html=u'', REQUEST=None):
        """ save sidebar HTML """
        self.sidebar_html = html
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('%s/sidebar?msg=%s' % (self.absolute_url(), 'HTML saved succesfully'))

    security.declareProtected('Manage Bitakora', 'save_css')

    def save_css(self, css=u'', REQUEST=None):
        """ save CSS """
        doc = getattr(self, 'blog.css')
        doc.update_data(css)

        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('%s/template?msg=%s' % (self.absolute_url(), 'CSS edited succesfully'))

    security.declareProtected('Manage Bitakora', 'select_template')

    def select_template(self, template, REQUEST=None):
        """ select an existing template """
        if not template in self.templates.objectIds():
            if REQUEST is not None:
                return REQUEST.RESPONSE.redirect('%s/template?msg=%s' % (self.absolute_url(), 'Selected template does not exist'))
            else:
                return

        obj = getattr(self.templates[template], 'blog.css').data
        current = getattr(self, 'blog.css')
        current.update_data(obj)

        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('%s/template?msg=%s' % (self.absolute_url(), 'Template changed succesfully'))

    security.declarePublic('inCommunity')

    def inCommunity(self):
        """ Return whether this Bitakora is in a Bitakora community """
        if self.getParentNode().meta_type == 'BitakoraCommunity':
            return 1
        return 0

    security.declarePublic('showYearMonth')

    def showYearMonth(self, yearmonth):
        """ convert 200512 to December 2005 """
        months = {
        '01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'
        }

        #ym = yearmonth.encode('utf-8')
        ym = yearmonth
        year = ym[:4]
        month = ym[4:]
        return self.gettext('%(year)s %(month)s') % {'month': self.gettext(months[month]), 'year': year}

    security.declarePublic('commentsAllowed')

    def commentsAllowed(self):
        """ Are comments allowed? """
        return self.comment_allowed

    security.declarePublic('commentsModerated')

    def commentsModerated(self):
        """ Are comments moderated? """
        return self.comment_allowed == 2

    security.declarePublic('commentsNotAllowed')

    def commentsNotAllowed(self):
        """ Are not comments allowed? """
        return not self.comment_allowed

    referencesAllowed = commentsAllowed
    referencesModerated = commentsModerated
    referencesNotAllowed = commentsNotAllowed

    security.declareProtected('Manage Bitakora', 'users')

    def users(self):
        """ Users """
        users = self.users_with_local_role('Blogger')
        if users:
            return users[0]
        return ''

    security.declarePublic('getUnpublishedComments')

    def getUnpublishedComments(self, size=None):
        """ get unpublished comments """
        if size is not None:
            return self.Catalog(meta_type='Comment',
                                published=0,
                                sort_on='date',
                                sort_order='descending',
                                sort_limit=size)
        else:
            return self.Catalog(meta_type='Comment',
                                published=0,
                                sort_on='date',
                                sort_order='descending')

    security.declarePublic('getPublishedComments')

    def getPublishedComments(self, size=None):
        """ get published comments """
        if size is not None:
            return self.Catalog(meta_type='Comment',
                                published=1,
                                sort_on='date',
                                sort_order='descending',
                                sort_limit=size)
        else:
            return self.Catalog(meta_type='Comment',
                                published=1,
                                sort_on='date',
                                sort_order='descending')

    security.declarePublic('getComments')

    def getComments(self, size=None):
        """ get comments """
        if size is not None:
            return self.Catalog(meta_type='Comment',
                                sort_on='date',
                                sort_order='descending',
                                sort_limit=size)
        else:
            return self.Catalog(meta_type='Comment',
                                sort_on='date',
                                sort_order='descending')

    security.declarePublic('getUnpublishedReference')

    def getUnpublishedReferences(self, size=None):
        """ get unpublished References """
        if size is not None:
            return self.Catalog(meta_type='Reference',
                                published=0,
                                sort_on='date',
                                sort_order='descending',
                                sort_limit=size)
        else:
            return self.Catalog(meta_type='Reference',
                                published=0,
                                sort_on='date',
                                sort_order='descending')

    security.declarePublic('getPublishedReferences')

    def getPublishedReferences(self, size=None):
        """ get published References """
        if size is not None:
            return self.Catalog(meta_type='Reference',
                                published=1,
                                sort_on='date',
                                sort_order='descending',
                                sort_limit=size)
        else:
            return self.Catalog(meta_type='Reference',
                                published=1,
                                sort_on='date',
                                sort_order='descending')

    security.declarePublic('getReferences')

    def getReferences(self, size=None):
        """ get References """
        if size is not None:
            return self.Catalog(meta_type='Reference',
                                sort_on='date',
                                sort_order='descending',
                                sort_limit=size)
        else:
            return self.Catalog(meta_type='Reference',
                                sort_on='date',
                                sort_order='descending')

    security.declarePrivate('createId')

    def createId(self, title):
        """ Create an id for a post based on its title """
        s1 = unicode(r"'\;/ &:ÀÁÂÄÇÈÊÉËÌÎÍÏÒÔÓÖÙÛÚÜÝŸàâáäçèêéëìîíïòôóöùûúüýÿÑñ", 'utf-8')
        s2 = unicode(r'-------aaaaceeeeiiiioooouuuuyyaaaaceeeeiiiioooouuuuyyNn', 'utf-8')

        # XXX This is not efficient at all
        # but string.maketrans and id.translate
        # don't work correctly with unicode strings....
        id = title.strip()
        for i in range(len(s1)):
            id = id.replace(s1[i], s2[i])

        id = ''.join([c for c in id if c in ok_chars])
        while id.startswith('-') or id.startswith('_') or id.startswith(' '):
            id = id[1:]

        while id.endswith('-') or id.endswith('_') or id.endswith(' '):
            id = id[:-1]

        while id.find('--') != -1:
            id = id.replace('--', '-')

        id = id.lower()
        if not id:
            return u'blogpost-%d' % self.postcount

        return u'-'.join(id.split(' '))

    security.declarePrivate('createNewId')

    def createNewId(self, oldid):
        """ Create a new id if the previous one was taken """
        if oldid[-1].isdigit():
            num = oldid.split('-')
            end = int(num[-1]) + 1
            return '-'.join(num[:-1]) + '-' + str(end)
        else:
            return oldid + '-1'

    security.declarePublic('prepareTags')

    def prepareTags(self, tags=[]):
        """ return tags to add and edit interfaces preview """
        from utils import prepareTags as prepTags
        return prepTags(tags)

    security.declareProtected('Manage Bitakora', 'importXML')

    def importXML(self, file, REQUEST=None):
        """ upload XML file with blog data """
        from XMLImporter import importXML as imp
        data = imp(xml=file.read())
        for post in data:
            id = self.manage_addPost(title=post['title'],
                                     author=post['author'],
                                     body=post['body'],
                                     tags=post['tags'],
                                     date=post['date'],
                                     not_clean=1,
                                     sendping=0)
            posta = self.get(id)
            for comment in post.get('comments', []):
                posta.manage_addComment(author=comment['author'],
                                        body=comment['body'],
                                        url=comment['url'],
                                        email=comment['email'],
                                        date=comment['date'])

        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('%s/prefs?msg=%s' % (self.absolute_url(), 'XML file imported succesfully'))

    security.declareProtected('Manage Bitakora', 'migrate_comments')

    def migrate_comments(self):
        """ Migrate comment attribute url to author_url, not to clash with
            CatalogAware's url attribute
        """
        from logging import getLogger
        log = getLogger('migrate_comments')
        log.info('starting')
        for post in self.objectValues('Post'):
            for comment in post.objectValues('Comment'):
                if hasattr(comment, 'url') and \
                    not callable(getattr(comment, 'url')):
                    comment.author_url = comment.url
                    log.info('Migrated: %s - %s' % (comment.getId(),
                                                    comment.author_url))
                    delattr
        log.info('done')

    security.declareProtected('Manage Bitakora', 'migrate_tinymce')

    def migrate_tinymce(self):
        from logging import getLogger
        log = getLogger('migrate_tinymce')
        if 'TinyMCE' not in self.objectIds():
            log.info('Adding TinyMCE')
            self.manage_addProduct['ZTinyMCE'].manage_addZTinyMCE('TinyMCE', 'TinyMCE')
            maker = self.manage_addProduct['ZTinyMCE'].manage_addZTinyConfiguration
            for config in default_configurations:
                maker(config['name'], configuration=config['config'],
                      tinymce_instance_path='/'.join(self.TinyMCE.getPhysicalPath()),
                      title='Example configuration',
                      optimize=True)

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
        self.migrate_comments()
        self.migrate_tinymce()
        self.migrate_textindexng2()
        return 1

Globals.InitializeClass(Bitakora)
