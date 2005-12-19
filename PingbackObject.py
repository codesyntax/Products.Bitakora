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
from OFS.ObjectManager import ObjectManager
from OFS.Folder import Folder
from OFS.Traversable import Traversable
from PingMethodContainer import PingMethodContainer
from AccessControl import ClassSecurityInfo
from Globals import Persistent

__version__ = "$Revision: 0.01 $"

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