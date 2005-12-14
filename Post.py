# -*- coding: utf-8 -*-
# Zope modules
from Globals import package_home, Persistent, HTMLFile
import Globals
from AccessControl import ClassSecurityInfo
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2

# Catalog
from Products.ZCatalog.CatalogPathAwareness import CatalogPathAware

# Other stuff
import DateTime
from utils import addDTML, clean, cleanBody, cleanEmail, cleanURL, discoverPingbackUrl, makeXMLRPCCall
from utils import addDTML, addPythonScript, clean, cleanBody, prepareTags, cleanEmail, cleanURL, ok_chars

from urllister import URLLister
from Comment import Comment
from Reference import Reference

__version__ = "$Revision: 0.01 $"


def manage_addPost(self, title, author, body, tags=[], date=u'', publish=1, comment_allowed=1, REQUEST=None):
    """ Called from ZMI when creating new posts """
    if not title:
        return REQUEST.RESPONSE.redirect('%s/post?msg=%s' % (self.blogurl(), 'You must provide at least the title of the post'))
        
    newid = self.createId(title)
    newtitle = clean(title)
    newauthor = clean(author)
    newbody = cleanBody(self, body)
    newtags = prepareTags(tags)
    newdate = DateTime.DateTime(date)

    while hasattr(self, newid):
        newid = self.createNewId(newid)

    post = Post(newid, newtitle, newauthor, newbody, newtags, newdate, publish, comment_allowed)
      
    self._setObject(str(newid), post)
    post = self.get(newid)
    pingbackresults = post.postPingBacks(newbody) 
    res = post.sendPing()    
    
    if self.inCommunity():
        # We are in a Bitakora Community, so catalog the post there
        cat = self.getParentNode().get('Catalog', 'None')
        if cat is not None:
            cat.catalog_object(post, '/'.join(post.getPhysicalPath()))

    self.postcount = self.postcount + 1


    if REQUEST is not None:
        return REQUEST.RESPONSE.redirect('%s/admin?msg=%s' % (self.absolute_url(), 'Post added succesfully'))

    return self.manage_main(self, REQUEST)

class Post(CatalogPathAware, BTreeFolder2):
    """ Post class """
    meta_type = 'Post'

    from Comment import manage_addComment
    from Reference import manage_addPingback

    security = ClassSecurityInfo()
    #security.setDefaultAccess("allow")
    
    security.declareProtected('Add Bitakora Comment', 'manage_addComment')

    security.declareProtected('Manage Bitakora', 'edit')
    edit = HTMLFile('ui/Post_edit', globals())

    security.declarePrivate('__init__')
    def __init__(self, id, title, author, body, tags=[], date=u'', publish=1, comment_allowed=1, reference_allowed=1):
        """ """
        BTreeFolder2.__init__(self, id)
        self.id = str(id)
        self.title = title
        self.author = author
        self.body = body
        self.tags = [tag for tag in tags]
        self.date = date
        self.comment_allowed = comment_allowed
        self.reference_allowed = reference_allowed
        self.published = publish
        self.reindex_object()
        

    security.declareProtected('Manage Bitakora', 'manage_editPost')
    def manage_editPost(self, title, author, body, tags=[], date=u'', publish=1, comment_allowed=1, reference_allowed=1, REQUEST=None):
        """ Editor """

        self.title = title
        self.author = author
        self.body = cleanBody(self, body)
        self.tags = prepareTags(tags)
        self.date = DateTime.DateTime(date)
        self.comment_allowed = comment_allowed
        self.reference_allowed = reference_allowed
        self.published = publish
        self.reindex_object()
        pingbackresults = self.postPingBacks(self.body) 
        
        if self.inCommunity():
            # We are in a Bitakora Community, so catalog the post there
            cat = self.getParentNode().getParentNode().get('Catalog', 'None')
            if cat is not None:
                cat.catalog_object(self, '/'.join(self.getPhysicalPath()))                

        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('%s/edit?msg=%s' % (self.absolute_url(), 'Post edited succesfully'))

    security.declareProtected('Add Bitakora Comment', 'manage_editComment')
    def manage_editComment(self, author, email, url, body, date, id, publish=1, REQUEST=None):
        """ Editor """

        if REQUEST.has_key('delete'):
            self._delObject(id)
            if REQUEST is not None:
                return REQUEST.RESPONSE.redirect('%s/edit?msg=%s' % (self.absolute_url(), 'Comment deleted succesfully'))
        else:

            if not (id in self.commentIds()):
                if REQUEST is not None:
                    return REQUEST.RESPONSE.redirect('%s/edit?msg=%s' % (self.absolute_url(), 'Comment does not exists'))
    
            com = getattr(self, id)
            com.edit(author, email, url, body, date, publish)
            self.reindex_object()

            if REQUEST is not None:
                return REQUEST.RESPONSE.redirect('%s/edit?msg=%s' % (self.absolute_url(), 'Comment edited succesfully'))

    security.declarePrivate('postPingBacks')
    def postPingBacks(self, newbody):
        """ pingback """
        pingbackresults = []
        parser = URLLister()
        parser.feed(newbody)
        parser.close()
        urls = parser.urls
    
        for url in urls:
            url = str(url)
            result = self.sendPingback(url)
            pingbackresults.append((url, result))

        return pingbackresults

    security.declarePrivate('sendPingback')
    def sendPingback(self, url):
        pburl = discoverPingbackUrl(url)
        if pburl is not None:
            code = makeXMLRPCCall(serverURI=pburl, sourceURI=self.absolute_url(), targetURI=url)
            return code
        else:
            # No pingback is possible
            return 2

    security.declarePrivate('hasPingback')
    def hasPingback(self, sourceURI):
        for pb in self.referenceList():
            if sourceURI == pb.showURI():
                return 1

        return 0

    security.declarePrivate('deleteAllComments')
    def deleteAllComments(self):
        """ """
        for id in self.commentIds():
            self._delObject(id)

    security.declarePrivate('deleteAllReferences')
    def deleteAllReferences(self):
        """ """
        for id in self.referenceIds():
            self._delObject(id)

    security.declarePublic('index_html')
    def index_html(self,REQUEST=None):
        """ Each post is rendered usint posting_html template """
        return self.posting_html(self,REQUEST)

    security.declarePublic('showTitle')
    def showTitle(self):
        """ get the title """
        return self.title.encode('utf-8')

    security.declarePublic('showAuthor')
    def showAuthor(self):
        """ get the author """
        return self.author.encode('utf-8')

    security.declarePublic('showTags')
    def showTags(self):
        """ get the tags """
        return u' '.join(self.tags).encode('utf-8')
        
    security.declarePublic('tagList')
    def tagList(self):
        """ get the tag list """
        return [tag.encode('utf-8') for tag in self.tags]

    security.declarePublic('showDate')
    def showDate(self):
        """ get the date """
        return unicode(str(self.date)).encode('utf-8')

    security.declarePublic('showBody')
    def showBody(self):
        """ get the body """
        return self.body.encode('utf-8')

    security.declarePublic('canComment')
    def canComment(self):
        """ Are the comments on this post allowed? """
        return self.comment_allowed 

    security.declarePublic('canReference')
    def canReference(self):
        """ Are the references (trackbacks, pingbacks, ...)
            on this post allowed? """
        return self.reference_allowed
        
    security.declarePublic('commentsModerated')
    def commentsModerated(self):
        """ Return whether comments are moderated (coment_allowed == 2) or not """
        return self.comment_allowed == 2

    security.declarePublic('hidden')
    def hidden(self):
        """ is hidden? """
        return not self.published

    security.declarePublic('getId')
    def getId(self):
        """ get the id of the post """
        return self.id

    security.declarePrivate('commentIds')
    def commentIds(self):
        """ Get the comment ids """
        return self.objectIds('Comment')

    security.declarePrivate('referenceIds')
    def referenceIds(self):
        """ Get the reference ids """
        return self.objectIds('Reference')

    security.declareProtected('View', 'commentList')
    def commentList(self, all=0):
        """ get the comments of this post """
        if all:
            return self.objectValues('Comment')
        else:
            return [com for com in self.objectValues('Comment') if com.published]

    security.declareProtected('View', 'referenceList')
    def referenceList(self, all=0):
        """ get the references of this post """
        if all:
            return self.objectValues('Reference')
        else:
            return [com for com in self.objectValues('Reference') if com.published]

    security.declarePrivate('createCommentId')
    def createCommentId(self):
        """ create id """
        if len(self.commentList(all=1)) == 0:
            return 0
        else:
            return len(self.commentList(all=1))

    security.declarePrivate('createReferenceId')
    def createReferenceId(self):
        """ create id """
        if len(self.referenceList()) == 0:
            return 'r1'
        else:
            return 'r'+len(self.referenceList())

    security.declareProtected('View', 'numberOfComments')
    def numberOfComments(self):
        """ Method that returns the number of comments of this post """
        return unicode(str(len(self.commentList()))).encode('utf-8')

    security.declareProtected('View', 'numberOfReferences')
    def numberOfReferences(self):
        """ Method that returns the number of references of this post """
        return unicode(str(len(self.referenceList()))).encode('utf-8')

    security.declarePrivate('yearmonth')
    def yearmonth(self):
        """ for archive """
        date = self.date
        try:
            year = date.year()
            month = date.month()
            return u'%d%02d' % (year, month)
        except:
            return u''

    security.declareProtected('Manage Bitakora', 'sendPing')
    def sendPing(self):
        """ send Update nortifications for PING Servers """
        ret_l = []
        url = self.absolute_url()
        blog_name = self.blog_title()
        ping_servers = ['http://rpc.pingomatic.com']
        for pingurl in ping_servers:
            try:
                resp = self.send_ping(pingurl, blog_name, url)
            except Exception,e:
                resp = {}
                resp["message"] = str(e)
                ret_l.append( {"url":pingurl,"message":resp["message"]} )
        return ret_l

    security.declarePrivate('send_ping')
    def send_ping(self, serverurl, blogtitle, url):
        """ """
        from xmlrpclib import Server, Transport
        version_str = 'Bitakora 0.1Beta'
        title = blogtitle.encode('utf-8')
        svr = Server(serverurl)
        Transport.user_agent = version_str
        resp = svr.weblogUpdates.ping(title, url)
        return resp

    security.declarePublic('forgetPersonalInfo')
    def forgetPersonalInfo(self, REQUEST):
        """ Delete set cookies """
        if REQUEST is not None:
            for cookie in ['comment_author', 'comment_url', 'comment_email']:
                REQUEST.RESPONSE.expireCookie(cookie)
            
            return REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)

    def users(self):
        return None            

    security.declarePublic('commentsAllowed')
    def commentsAllowed(self):
        """ Are comments allowed? """
        return self.comment_allowed

    security.declarePublic('commentsModerated')        
    def commentsModerated(self):
        """ Are comments moderated? """
        return self.comment_allowed == 2

    security.declarePublic('commentsNotAllowed')        
    def commentsNotAllowed(self):
        """ Are not comments allowed? """
        return not self.comment_allowed            

Globals.InitializeClass(Post)