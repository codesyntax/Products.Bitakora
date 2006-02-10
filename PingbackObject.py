# -*- coding: utf-8 -*-
# (c) Copyright 2005, CodeSyntax <http://www.codesyntax.com>
# Authors: Mikel Larreategi <mlarreategi@codesyntax.com>
# See also LICENSE.txt

#$Id$


# Zope modules
from OFS.ObjectManager import ObjectManager
from OFS.Folder import Folder
from OFS.Traversable import Traversable
from PingMethodContainer import PingMethodContainer
from AccessControl import ClassSecurityInfo
from Globals import Persistent

__version__ = "$Revision$"

class PingbackObject(Folder):
    """ asdfsaf """
    meta_type = 'PingbackObject'
    security = ClassSecurityInfo()

    security.declarePublic('__init__')
    def __init__(self):
        """ Some stuff here """
        Folder.__init__(self)
        self.id = 'pingback'
        self._setObject('pingback', PingMethodContainer())

    security.declarePublic('getId')
    def getId(self):
        return self.id

    security.declarePublic('__call__')
    __call__ = None

    security.declarePublic('index_html')
    index_html = None