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

import Bitakora, BitakoraCommunity

def initialize(context):
    """ """
    # Register Bitakora
    context.registerClass(Bitakora.Bitakora,
                          constructors = (Bitakora.manage_addBitakoraForm,
                                          Bitakora.manage_addBitakora),
                          icon='img/icoBitakora.gif')

    # Register BitakoraCommunity
    context.registerClass(BitakoraCommunity.BitakoraCommunity,
                          constructors = (BitakoraCommunity.manage_addBitakoraCommunityForm,
                                          BitakoraCommunity.manage_addBitakoraCommunity),
                          icon='img/icoBitakoraCommunity.gif')

