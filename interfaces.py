from zope.interface import Interface
from zope.schema import Text, TextLine, Field, DateTime, List, URI

__version__ = '$Id'

class IBitakoraCommunity(Interface):
    """ Interface for BitakoraCommunity """
    title = TextLine(
        title = u"BitakoraCommunity title",
        description = u"BitakoraCommunity title",
        default = u"",
        required = True)
        
    admin_mail = TextLine(
        title = u"BitakoraCommunity administrator e-mail",
        description = u"BitakoraCommunity administrator e-mail",
        default = u"",
        required = True)
        
        
class IBitakora(Interface):
    """ Interface for Bitakora """

    title = TextLine(
        title = u"Bitakora title",
        description = u"Bitakora title",
        default = u"",
        required = True)
        
    subtitle = TextLine(
        title = u"Bitakora subtitle",
        description = u"Bitakora subtitle",
        default = u"",
        required = False)        

    description = Text(
        title = u"Description",
        description = u"A detailed description of the blog's contents.",
        default = u"",
        required = False)  

    contact_mail = TextLine(
        title = u"BitakoraCommunity administrator e-mail",
        description = u"BitakoraCommunity administrator e-mail",
        default = u"",
        required = True)
             
class IPost(Interface):
    """ Interface for Bitakora post """    
    
    title = TextLine(
        title = u"Blog entry title",
        description = u"Blog entry title.",
        default = u"",
        required = True)
        
    author = TextLine(
        title = u"Blog entry author",
        description = u"Blog entry author.",
        default = u"",
        required = True)                 

    body = Text(
        title = u"Blog entry content",
        description = u"Blog entry content.",
        default = u"",
        required = True)         
        
    date = DateTime(
        title = u'Blog entry date',
        description = u'Date and hour in which the post will be published',
        required = False)
    
    
    tags = List(
        title = u'Blog entry tags',
        description = u'Enter tags to categorize this blog entry',
        required = False)
        
class IComment(Interface):
    """ Interface for blog entry comments """
    author = TextLine(
        title = u"Comment author",
        description = u"Comment author.",
        default = u"",
        required = True)                 

    email = TextLine(
        title = u"Comment author's email",
        description = u"Comment author's email.",
        default = u"",
        required = True)
        
    url = URI(
        title = u"Comment author's URL",
        description = u"Comment author's URL.",
        default = u'',
        required = False)


    author = TextLine(
        title = u"Blog entry author",
        description = u"Blog entry author.",
        default = u"",
        required = True)                 


    body = Text(
        title = u"Blog entry content",
        description = u"Blog entry content.",
        default = u"",
        required = True)         
        

        
               
                  
