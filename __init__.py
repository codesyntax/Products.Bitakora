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