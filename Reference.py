# -*- coding: utf-8 -*-
# (C) Copyright 2005, CodeSyntax <http://www.codesyntax.com>
# Authors: Mikel Larreategi <mlarreategi@codesyntax.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

# Zope modules
from Globals import package_home
import Globals
from OFS.SimpleItem import SimpleItem
from AccessControl import ClassSecurityInfo

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