# -*- coding: utf-8 -*-
# (c) Copyright 2005, CodeSyntax <http://www.codesyntax.com>
# Authors: Mikel Larreategi <mlarreategi@codesyntax.com>
# See also LICENSE.txt

#$Id$

# Zope modules
import Globals
from OFS.SimpleItem import SimpleItem
from AccessControl import ClassSecurityInfo

# Catalog
from Products.ZCatalog.CatalogPathAwareness import CatalogPathAware
from Products.PythonScripts.standard import url_quote

# Other stuff
import DateTime
from utils import clean, cleanBody, cleanEmail, cleanURL, notifyByEmail

__version__ = "$Revision$"

def manage_addComment(self, author, body, url='', email='', date=None, bitakora_cpt='', random_cpt='', captcha_zz=0, REQUEST=None):
    """ Called from HTML form when commenting """
    from utils import checkCaptchaValue
    if not captcha_zz:
        if not checkCaptchaValue(random_cpt, bitakora_cpt):
            if REQUEST is not None:
                return REQUEST.RESPONSE.redirect(self.absolute_url()+u'?msg=%s&body=%s&comment_author=%s&comment_email=%s&comment_url=%s#bitakora_cpt_control' % (self.gettext('Are you a bot? Please try again...'), url_quote(body.encode('utf-8')), url_quote(author.encode('utf-8')), url_quote(email.encode('utf-8')), url_quote(url.encode('utf-8'))))
            
            return None
        
    newauthor = clean(author)
    newbody = cleanBody(self, body)
    newurl = cleanURL(url)
    newemail = cleanEmail(email)
    if date is None:
        newdate = DateTime.DateTime()
    else:
        newdate = DateTime.DateTime(date)           
    newid = self.createCommentId()
    publish = 1
    if self.commentsModerated():
        publish = 0
    comment = Comment(newid, newauthor, newemail, newurl, newbody, newdate, self.getId(), publish)

    self._setObject(str(newid), comment)
    
    comment = getattr(self, str(newid))
    
    try:
        mailhost=getattr(self,self.superValues('Mail Host')[0].id)
        from EpozPostTidy import cleanHTML
        
        mTo = self.contact_mail
        if self.inCommunity():
            mFrom = self.admin_mail
        else:
            mFrom = self.contact_mail
            
        variables = {}            
        variables['from'] = mFrom.encode('utf-8')
        variables['to'] = mTo.encode('utf-8')
        variables['comment_author'] = newauthor.encode('utf-8')
        variables['comment_email'] = newemail.encode('utf-8')
        variables['comment_url'] = newurl.encode('utf-8')
        variables['comment_body'] = cleanHTML(newbody).encode('utf-8')
        variables['comment_address'] = comment.absolute_url()
            
        mSubj = self.gettext('New comment in your blog!') 
        mMsg = self.comment_email_template(self, **variables)

        notifyByEmail(mailhost, mTo.encode('utf-8'), mFrom.encode('utf-8'), mSubj.encode('utf-8'), mMsg)
    except:
        # If there is no MailHost, or other error happened
        # there won't be e-mail notifications
        pass
    

    #set cookie
    if REQUEST and REQUEST.form.has_key('setcookie'):
        resp = REQUEST.RESPONSE
        path = "/"
        gtime = DateTime.DateTime() + 365
        exp = gtime.strftime('%A, %d-%b-%y %H:%M:%S GMT')

        resp.setCookie('comment_author',author.encode('utf-8'),expires=exp,path=path)
        resp.setCookie('comment_email',email.encode('utf-8'),expires=exp,path=path)
        resp.setCookie('comment_url',url.encode('utf-8'),expires=exp,path=path)

    if REQUEST is not None:
        return REQUEST.RESPONSE.redirect(self.absolute_url())

    return newid

class Comment(CatalogPathAware, SimpleItem):
    """ Comment class """
    meta_type = 'Comment'
    
    security = ClassSecurityInfo()

    security.declarePrivate('__init__')
    def __init__(self, id, author, email, url, body, date, postid, publish=1):
        """ Constructor """
        self.id = str(id)
        self.author = author
        self.email = email
        self.url = url
        self.body = body
        self.date = date
        self.published = publish
        self.postid = postid

    security.declareProtected('Manage Bitakora', 'edit')
    def edit(self, author, email, url, body, date, publish=1, REQUEST=None):
        """ Editor """
        self.author = author
        self.email = email
        self.url = url
        self.body = cleanBody(self, body)
        self.date = DateTime.DateTime(date)
        self.published = publish
        self.reindex_object()
        if REQUEST is not None:
            url = REQUEST.HTTP_REFERER.split('?')[0]
            return REQUEST.RESPONSE.redirect(url+'?msg=%s' % 'Comment edited successfully')

    security.declareProtected('Manage bitakora', 'delete')
    def delete(self, REQUEST):
        """ delete this comment """
        REQUEST['delete'] = 1
        self.getParentNode().manage_editComment(author='', email='', url='', body='', date='', id=self.id, REQUEST=REQUEST)
        if REQUEST is not None:
            url = REQUEST.HTTP_REFERER.split('?')[0]
            return REQUEST.RESPONSE.redirect(url+'?msg=%s' % 'Comment deleted successfully')

    security.declarePublic('index_html')
    def index_html(self,REQUEST=None):
        """ Each post is rendered usint comment_body template """
        return self.getParentNode().index_html(REQUEST)
        
    security.declarePublic('hidden')
    def hidden(self):
        """ return true if this comment is not published """
        return not self.published

    security.declarePublic('showAuthor')
    def showAuthor(self):
        """ get the author """
        return self.author

    security.declarePublic('showEmail')
    def showEmail(self):
        """ get the email """
        return self.email

    security.declarePublic('showURL')
    def showURL(self):
        """ get the url """
        return self.url

    security.declarePublic('showDate')
    def showDate(self):
        """ get the date """
        return unicode(str(self.date))

    security.declarePublic('showBody')
    def showBody(self):
        """ get the body """
        return self.body

    security.declarePublic('getId')
    def getId(self):
        """ get the id of the Comment """
        return self.id

    security.declarePublic('absolute_url')
    def absolute_url(self):
        """ """
        return self.getParentNode().absolute_url()+'#comment'+self.id

    security.declarePublic('postTitle')
    def postTitle(self):
        return self.showTitle()

Globals.InitializeClass(Comment)