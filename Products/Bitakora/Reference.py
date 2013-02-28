# -*- coding: utf-8 -*-
# (c) Copyright 2005, CodeSyntax <http://www.codesyntax.com>
# Authors: Mikel Larreategi <mlarreategi@codesyntax.com>
# See also LICENSE.txt

# Zope modules
import Globals
from OFS.SimpleItem import SimpleItem
from AccessControl import ClassSecurityInfo

# Catalog
from Products.ZCatalog.CatalogPathAwareness import CatalogAware

# Other stuff
import DateTime
from utils import clean


def manage_addPingback(self, sourceTitle, sourceURI, sourceExcerpt):
    """ Add a pingback """
    from utils import isPingbackSpam

    if isPingbackSpam(sourceTitle, sourceURI, sourceExcerpt,
                      self.blogurl(), self.REQUEST):
        try:
            return self.REQUEST.RESPONSE.redirect('http://www.google.com')
        except:
            return 0

    id = self.createReferenceId()
    newTitle = clean(sourceTitle)
    newURI = clean(sourceURI)
    newExcerpt = clean(sourceExcerpt)
    pingback = Reference(id, newTitle, newURI, newExcerpt, self.getId())
    self._setObject(id, pingback)
    return 1


class Reference(CatalogAware, SimpleItem):
    """ Reference class """
    meta_type = 'Reference'

    security = ClassSecurityInfo()
    #security.setDefaultAccess("allow")

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

    security.declareProtected('Manage Bitakora', 'edit')

    def edit(self, title, uri, excerpt, publish=1, REQUEST=None):
        """ Editor """
        self.title = title
        self.uri = uri
        self.excerpt = excerpt
        self.published = publish
        self.reindex_object()
        if REQUEST is not None:
            url = REQUEST.HTTP_REFERER.split('?')[0]
            return REQUEST.RESPONSE.redirect(url+'?msg=%s' % 'Reference edited successfully')

    security.declareProtected('Manage bitakora', 'delete')

    def delete(self, REQUEST):
        """ delete this comment """
        REQUEST['delete'] = 1
        self.getParentNode()._delObject(self.id)
        if REQUEST is not None:
            url = REQUEST.HTTP_REFERER.split('?')[0]
            return REQUEST.RESPONSE.redirect(url+'?msg=%s' % 'Reference deleted successfully')

    security.declarePublic('index_html')

    def index_html(self,REQUEST=None):
        """ Each post is rendered usint Reference_body template """
        return self.getParentNode().index_html(REQUEST)

    security.declarePublic('hidden')

    def hidden(self):
        """ return true if this comment is not published """
        return not self.published

    security.declarePublic('showTitle')

    def showTitle(self):
        """ get the title """
        return self.title

    security.declarePublic('showDate')

    def showDate(self):
        """ get the date """
        return unicode(str(self.date))

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
        return self.getParentNode().absolute_url() + '#' + self.id

Globals.InitializeClass(Reference)
