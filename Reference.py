# Zope modules
from Globals import package_home, Persistent
import Globals
from OFS.SimpleItem import SimpleItem
from OFS.Traversable import Traversable
from Acquisition import Implicit
from AccessControl import ClassSecurityInfo
from BTrees.IOBTree import IOBTree

# Catalog
from Products.ZCatalog.CatalogPathAwareness import CatalogPathAware

# Other stuff
import DateTime
from utils import addDTML, addPythonScript, clean, cleanBody, prepareTags, cleanEmail, cleanURL, ok_chars
__version__ = "$Revision: 0.01 $"

def manage_addPingback(self, sourceTitle, sourceURI, sourceExcerpt):
    """ Add a pingback """
    id = self.createReferenceId()
    newTitle = clean(sourceTitle)
    newURI = clean(sourceURI)
    newExcerpt = clean(sourceExcerpt)
    pingback = Reference(id, newTitle, newURI, newExcerpt, self.getId())
    self._setObject(id, pingback)
        

class Reference(CatalogPathAware, SimpleItem):
    """ asdfklasfasldfj """

    security = ClassSecurityInfo()
    security.setDefaultAccess("allow")

    meta_type = 'Reference'

    security.declarePrivate('__init__')
    def __init__(self, id, title, uri, excerpt, postid, publish=1):
        """ Constructor """
        self.id = str(id)
        self.title = title
        self.uri = uri
        self.excerpt = excerpt
        self.published = publish
        self.postid = postid
        self.date = DateTime.DateTime()

    security.declarePrivate('edit')
    def edit(self, title, uri, excerpt, publish=1):
        """ Editor """
        self.title = title
        self.uri = uri
        self.excerpt = excerpt
        self.published = publish

    security.declarePublic('index_html')
    def index_html(self,REQUEST=None):
        """ Each post is rendered usint Reference_body template """
        return self.getParentNode().index_html(REQUEST)

    security.declarePublic('showTitle')
    def showTitle(self):
        """ get the title """
        return self.title

    security.declarePublic('showDate')
    def showDate(self):
        """ get the date """
        return self.date

    security.declarePublic('showBody')
    def showURI(self):
        """ get the uri """
        return self.uri

    security.declarePublic('showExcerpt')
    def showExcerpt(self):
        """ get the excerpt """
        return self.excerpt

    security.declarePublic('getId')
    def getId(self):
        """ get the id of the Reference """
        return self.id

    security.declarePublic('absolute_url')
    def absolute_url(self):
        """ """
        return self.getParentNode().absolute_url()+'#reference'+self.id
        
Globals.InitializeClass(Reference)        