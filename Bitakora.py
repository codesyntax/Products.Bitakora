# -*- coding: utf-8 -*-
# Zope modules
from Globals import HTMLFile
import Globals
from zLOG import LOG, ERROR
from AccessControl import ClassSecurityInfo
from Acquisition import Implicit, aq_base
from BTrees.IOBTree import IOBTree
from BTrees.OOBTree import OOBTree
from OFS.Folder import Folder
from OFS.ObjectManager import ObjectManager
from Products.PythonScripts.PythonScript import manage_addPythonScript
from Products.PythonScripts.PythonScript import PythonScript
from Products.ExternalMethod.ExternalMethod import manage_addExternalMethod

# Catalog
from Products.ZCatalog import ZCatalog
from Products.ZCatalog.CatalogPathAwareness import CatalogPathAware
   
from Products.Localizer.MessageCatalog import MessageCatalog

# To add ZCatalog FieldIndex and TextIndexNG2
from ZPublisher.HTTPRequest import record

# BTreeFolder2
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2

# Other stuff
import DateTime, string

# Own modules
from utils import addDTML, addPythonScript, clean, cleanBody, prepareTags, cleanEmail, cleanURL, ok_chars, createId, createNewId
from urllister import URLLister
from PingMethodContainer import PingMethodContainer



__version__ = "$Revision: 0.01 $"

manage_addBitakoraForm = HTMLFile('ui/Bitakora_add', globals())

def manage_addBitakora(self, id, title, subtitle, contact_mail, description=u'', REQUEST=None):
    """ Method called from ZMI to create a new Bitakora """
    import Bitakora
    sq = Bitakora.Bitakora(id, title, subtitle, description, contact_mail)
    self._setObject(id, sq)
    sq = getattr(self, id)
    
    if REQUEST is not None and REQUEST.has_key('image'):
        ext = image.filename.split('.')[-1]
        imgid = 'image.%s' % ext
        sq.manage_addImage(imgid, REQUEST.get('image'))
        sq.imageUrl = '%s/%s' % (sq.absolute_url(), imgid)
    
    elif REQUEST is None or not REQUEST.has_key('image'):
        from random import random
        
        imgnum = (int(random()*10) % 3) + 1
        file = 'face0%s.gif' % imgnum
        file_path = Globals.package_home(globals())
        f=open(file_path+'/ui/communityTemplates/'+file,'rb')     
        contents=f.read()     
        f.close()     
        title=''     
        tlen = len(contents)
        imgid = 'image.gif'
        new_id = sq.manage_addImage(imgid,contents,title=title)
        sq.imageUrl = '%s/%s' % (sq.absolute_url(), imgid)
        
    # Add a MessageCatalog if we are a standalone Bitakora
    # if not, the BitakoraCommunity MessageCatalog will handle
    # the messages
    if self.meta_type == 'BitakoraCommunity':
        sq._delObject('gettext')
        self.Catalog.catalog_object(sq, '/'.join(sq.getPhysicalPath()))
    
    if REQUEST is not None:
        return self.manage_main(self, REQUEST)

class Bitakora(BTreeFolder2, CatalogPathAware):
    """ Bitakora is a new blog product for Zope
        based on Squishdot and COREBlog """
    from Post import manage_addPost 
    
    meta_type = 'Bitakora'  

    __ac_roles__ = ('Blogger',)

    security = ClassSecurityInfo()

    security.setPermissionDefault('Manage Bitakora',     ('Blogger', 'Manager',))
    security.setPermissionDefault('Add Bitakora Comment',('Anonymous','Manager'))
                                    
    _properties = ({'id':'title', 'type': 'ustring', 'mode': 'w'},
                   {'id':'subtitle', 'type':'ustring', 'mode':'w'},
                   {'id':'contact_mail', 'type':'ustring', 'mode':'w'},
                   {'id':'management_page_charset','type':'ustring', 'mode':'w'},
                   {'id':'sidebar_html', 'type':'utext', 'mode':'w'},
                   {'id':'description', 'type':'utext', 'mode':'w'})

    manage_options=({'label':'Contents', 'action':'manage_main'},
                    {'label':'View', 'action':'index_html'},
                    {'label':'Security', 'action':'manage_access'},
                    {'label':'Undo', 'action':'manage_UndoForm'},)

    archive = HTMLFile('ui/archive', globals())
    comment_body = HTMLFile('ui/comment_body', globals())
    comment_form = HTMLFile('ui/comment_form', globals())
    entry_body = HTMLFile('ui/entry_body', globals())
    entry_preview = HTMLFile('ui/entry_preview', globals())
    index_html = HTMLFile('ui/index_html', globals())
    localmenu = HTMLFile('ui/localmenu', globals())
    admin_header = HTMLFile('ui/admin_header', globals())
    about = HTMLFile('ui/about', globals())
    contents = HTMLFile('ui/contents', globals())
    downloadTXT = HTMLFile('ui/downloadTXT', globals())
    logged_in = HTMLFile('ui/logged_in', globals())
    logged_out = HTMLFile('ui/logged_out', globals())
    login_form = HTMLFile('ui/login_form', globals())
    posting_html = HTMLFile('ui/posting_html', globals())
    recent_comments = HTMLFile('ui/recent_comments', globals())
    reference_body = HTMLFile('ui/reference_body', globals())
    Bitakora_comment_js = HTMLFile('ui/Bitakora_comment.js', globals())
    Bitakora_edit_js = HTMLFile('ui/Bitakora_edit.js', globals())
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
    
    security.declareProtected('Manage Bitakora', 'props')
    props = HTMLFile('ui/Blog_edit', globals())

    security.declareProtected('Manage Bitakora', 'sidebar')
    sidebar = HTMLFile('ui/manage_sidebar', globals())    
    
    security.declareProtected('Manage Bitakora', 'template')
    template = HTMLFile('ui/manage_template', globals())
    
    security.declareProtected('Manage Bitakora', 'download')
    download = HTMLFile('ui/manage_download', globals())

    admin_options = ['admin', 'post', 'sidebar', 'props', 'template', 'download']

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
        catalog = ZCatalog.ZCatalog('Catalog', 'Catalog')
        self._setObject('Catalog', catalog)
        self._buildIndexes()
        self._addMethods()
        self._setObject('pingback', PingMethodContainer())
        self.postcount = 0
        self._links = IOBTree()
        # if 0 not allowed, 1 allowed, 2 allowed but moderated
        self.comment_allowed = 1
        self.imageUrl = None
        
    security.declareProtected('View', 'searchResults')
    def searchResults(self, **kw):
        """ Call the Catalog """
        return self.Catalog.searchResults(kw)

    security.declareProtected('View', 'all')
    def all(self, REQUEST=None, **kw):
        """ Just a wrapper around call """
        return self.Catalog(REQUEST, **kw)

    security.declareProtected('Manage Bitakora', 'editBlog')
    def editBlog(self, title, subtitle, contact_mail, description, comment_allowed, image=None, REQUEST=None):
        """ editing method """
        self.title = title
        self.subtitle = subtitle
        self.contact_mail = contact_mail
        self.description = description
        self.comment_allowed = comment_allowed
        if image.read():
            ext = image.filename.split('.')[-1]
            imgid = 'image.%s' % ext
            original_id = self.imageUrl.split('/')[-1]
            original_img = self.get(original_id).data
            self._delObject(original_id)
        
            image.seek(0)           
            self.manage_addImage(imgid, image)
            
            img = self.get(imgid)
            if img.height > 65 and img.width > 65:
                self._delObject(imgid)
                self.manage_addImage(original_id, original_img)
                self.imageUrl = '%s/%s' % (self.absolute_url(), original_id)
                if REQUEST is not None:
                    return REQUEST.RESPONSE.redirect('%s/props?msg=%s' % (self.blogurl(), 'Your image is too large. Try with a smaller one'))
            
            self.imageUrl = '%s/%s' % (self.absolute_url(), imgid)
                        
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect('%s/props?msg=%s' % (self.blogurl(), 'Properties edited succesfully'))

    security.declarePrivate('_buildIndexes')
    def _buildIndexes(self):
        """ Stuff to create Catalog indexes """
        # delete any existing indexes
        for name in self.Catalog.indexes():
            self.Catalog.delIndex(name)

        # add the default indexes
        for (name,index_type) in [('meta_type', 'FieldIndex'),
                                  #('author', 'FieldIndex'),
                                  #('body', 'TextIndex'),
                                  #('title', 'TextIndex'),
                                  #('subtitle', 'TextIndex'),
                                  ('published', 'FieldIndex'),
                                  ('date', 'DateIndex'),
                                  ('tags', 'KeywordIndex'),
                                  ('yearmonth', 'KeywordIndex')]:
            self.Catalog.addIndex(name,index_type)

        extras = record()
        extras.splitter_single_chars = 1
        extras.default_encoding = 'UTF-8'
        extras.splitter_separators = '.+-_@'
        self.Catalog.manage_addIndex('author', 'TextIndexNG2', extra=extras)
        self.Catalog.manage_addIndex('title', 'TextIndexNG2', extra=extras)
        self.Catalog.manage_addIndex('body', 'TextIndexNG2', extra=extras)
        self.Catalog.manage_addIndex('excerpt', 'TextIndexNG2', extra=extras)

        # delete the default metadata columns
        for name in self.Catalog.schema():
            self.Catalog.delColumn(name)

        # Add the meta data columns for search results
        # hau ez dakit... Squishdot-etik kopiatu dut
        # supongo katalogoaren bilaketa ostean getObject
        # egiten ez ibiltzeko dela
        """
        for name in ['id','title','author','body','tags','date']:
            self.Catalog.addColumn(name,'')
        """

    security.declarePrivate('_addMethods')
    def _addMethods(self):
        """ Just to have all methods adding something extra
            to the ZMI together """
        file_path = Globals.package_home(globals())

        try:
            # old MessageCatalog
            self._setObject('gettext', MessageCatalog('gettext', '', ('en',)))
        except:
            # new MessageCatalog
            self._setObject('gettext', MessageCatalog('gettext', '', 'en', ['en']))
        
        # Add a special tag.py script which makes use of traverse subpath
        self._setObject('tag', PythonScript('tag'))
        tag = getattr(self, 'tag')
        f=open(file_path+'/tag.py')     
        data = f.read()
        f.close()
        tag.ZPythonScript_edit('', data)

        # Add a feed.xml file with the RSS feed
        addDTML(self,'feed.xml','','ui/feed.xml')
 
        # Add the CSS file       
        self.manage_addFile('blog.css')
        css = getattr(self, 'blog.css')
        f = open(file_path+'/ui/blog.css')
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
            return self.Catalog.searchResults(meta_type='Post', published=1, date=DateTime.DateTime(), date_usage='range:max', sort_on='date', sort_order='descending', sort_limit=size)
        else:
            return self.Catalog.searchResults(meta_type='Post', published=1, date=DateTime.DateTime(), date_usage='range:max', sort_on='date', sort_order='descending')
            
 
        
        
    security.declarePublic('last_post')
    def last_post(self):
        """ return the last published post """
        posts = self.Catalog.searchResults(meta_type='Post', size=1, sort_on='date', sort_order='descending')
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
        return unicode(self.title, 'utf-8').encode('utf-8')

    security.declarePublic('title_or_id')
    def title_or_id(self):
        """ title or id """
        return self.title or self.id

    security.declarePublic('blogurl')
    def blogurl(self):
        """ blog url """
        return self.absolute_url()

    security.declarePublic('tagsAndPixels')
    def tagsAndPixels(self):
        """ returns a dictionary with (tag, pixelSize) pairs
            based on number of posts cataloged with the tags """

        tags = self.Catalog.uniqueValuesFor('tags')
        zenbat = {}
        for tag in tags:
            tagkop = self.Catalog.searchResults(tags=tag)
            zenbat[tag.encode('utf-8')] = len(tagkop)

        maxpx = 2.30
        minpx = 0.70
        difpx = maxpx-minpx
        
        if zenbat.values():       
            maxnum = max(zenbat.values())
            minnum = max(zenbat.values())
        else:
            maxnum = 0
            minnum = 0
      

        hiz = {}
        for k,v in zenbat.items():
            hiz[k] = float(difpx*v/maxnum)+minpx

        return hiz

    security.declarePublic('lastComments')
    def lastComments(self, size=10):
        return self.Catalog.searchResults(meta_type='Comment', sort_on='date', sort_order='reverse', published=1)

    security.declarePublic('lastReferences')
    def lastReferences(self, size=10):
        return self.Catalog.searchResults(meta_type='Reference', sort_on='date', sort_order='reverse', published=1)

    security.declarePrivate('blog')
    def blog(self):
        return self

    security.declareProtected('Manage Bitakora', 'addLink')
    def addLink(self, url, title, REQUEST=None):
        """ Add a new link in link menu """
        try:
            max = self._links.maxKey()
            self._links[max+1] = (url, title)
        except ValueError:
            self._links[0] = (url, title)
        except:
            min = self._links.minKey()
            self._links[min-1] = (url, title)
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect('%s/sidebar?msg=%s' % (self.blogurl(), self.gettext('Link added succesfully')))

    security.declareProtected('Manage Bitakora', 'removeLink')
    def removeLink(self, key=None, REQUEST=None):
        """ remove link from link menu """
        if key is not None:
            try:
                del self._links[key]
            except:
                if REQUEST is not None:
                    REQUEST.RESPONSE.redirect('%s/sidebar?msg=%s' % (self.blogurl(), self.gettext('Error when deleting selected link')))
            if REQUEST is not None:        
                REQUEST.RESPONSE.redirect('%s/sidebar?msg=%s' % (self.blogurl(), self.gettext('Selected link was removed succesfully')))
        else:
            if REQUEST is not None:
                REQUEST.RESPONSE.redirect('%s/sidebar?msg=%s' % (self.blogurl(), self.gettext('What?')))

    security.declarePublic('showLinks')
    def showLinks(self):
        """ show links """
        elems = []
        for key in self._links.keys():
            url = self._links.get(key)[0]
            title = self._links.get(key)[1]
            elems.append({'url':url, 'title':title, 'key':key})

        return elems
        
    security.declareProtected('Manage Bitakora', 'save_sidebar_html')
    def save_sidebar_html(self, html=u'', REQUEST=None):
        """ save sidebar HTML """
        self.sidebar_html = html
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect('%s/sidebar?msg=%s' % (self.absolute_url(), self.gettext('HTML saved succesfully')))        
        
        
    security.declareProtected('Manage Bitakora', 'save_css')
    def save_css(self, css=u'', REQUEST=None):
        """ save CSS """       
        doc = getattr(self, 'blog.css')
        doc.update_data(css)
        
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect('%s/template?msg=%s' % (self.absolute_url(), self.gettext('CSS edited succesfully')))
            
    security.declareProtected('Manage Bitakora', 'select_template')
    def select_template(self, template, REQUEST=None):
        """ select an existing template """
        if not template in self.templates.objectIds():
            if REQUEST is not None:
                REQUEST.RESPONSE.redirect('%s/template?msg=%s' % (self.absolute_url(), self.gettext('Selected template does not exist')))
            else:
                return
        
        obj = getattr(self.templates[template], 'blog.css').data
        current = getattr(self, 'blog.css')
        current.update_data(obj)
        
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect('%s/template?msg=%s' % (self.absolute_url(), self.gettext('Template changed succesfully')))
            
    security.declarePublic('inCommunity')            
    def inCommunity(self):
        """ Return whether this Bitakora is in a Bitakora community """            
        if self.getParentNode().meta_type == 'BitakoraCommunity':
            return 1
        return 0      
        
    security.declarePublic('showDescription')
    def showDescription(self):
        return self.description.encode('utf-8')
        
    security.declarePublic('showYearMonth')
    def showYearMonth(self, yearmonth):
        """ convert 200512 to December 2005 """
        months = {
        '01' : 'January',
        '02' : 'February',
        '03' : 'March',
        '04' : 'April',
        '05' : 'May',
        '06' : 'June',
        '07' : 'July',
        '08' : 'August',
        '09' : 'September',
        '10' : 'October',
        '11' : 'November',
        '12' : 'December'
        }
        year = yearmonth[:4]
        month = yearmonth[4:]
        return (self.gettext('%(month)s %(year)s') % {'month':self.gettext(months[month]), 'year':year}).encode('utf-8')
     
     
    def commentsAllowed(self):
        """ Are comments allowed? """
        return self.comment_allowed
        
    def commentsModerated(self):
        """ Are comments moderated? """
        return self.comment_allowed == 2
        
    def commentsNotAllowed(self):
        """ Are not comments allowed? """
        return not self.comment_allowed
     
    def users(self):
        """ Users """
        users = self.users_with_local_role('Blogger')
        if users:
            return users[0]
        return ''
     
    security.declarePublic('fix')
    def fix(self):
        """ general method for fixing things """
        return None


Globals.InitializeClass(Bitakora)



