# -*- coding: utf-8 -*-
# (c) Copyright 2005, CodeSyntax <http://www.codesyntax.com>
# Authors: Mikel Larreategi <mlarreategi@codesyntax.com>
#
# Portions Copyright (c) 2003-2005 Atsushi Shibata
#
# See also LICENSE.txt


#$Id$

# Zope modules
from Globals import HTMLFile
import Globals
from AccessControl import ClassSecurityInfo
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2

# Catalog
from Products.ZCatalog.CatalogPathAwareness import CatalogAware

# Other stuff
import DateTime
from utils import clean, cleanBody
from utils import prepareTags
from utils import sendPing, postPingBacks
from future import Future


def manage_addPost(self, title, author, body, tags=[],
                  date=DateTime.DateTime(), publish=1,
                  comment_allowed=1, not_clean=0, sendping=1, REQUEST=None):
    """ Called from ZMI when creating new posts """
    if not title and REQUEST is not None:
        return REQUEST.RESPONSE.redirect('%s/post?msg=%s' % (self.blogurl(), 'You must provide at least the title of the post'))

    newid = self.createId(title)
    newtitle = clean(title)
    newauthor = clean(author)
    if not_clean:
        newbody = body
    else:
        newbody = cleanBody(self, body)
    newtags = prepareTags(tags)
    newdate = DateTime.DateTime(date)

    while hasattr(self, newid):
        newid = self.createNewId(newid)

    post = Post(newid, newtitle, newauthor, newbody,
                newtags, newdate, publish, comment_allowed)

    self._setObject(str(newid), post)
    post = self.get(newid)

    if self.inCommunity():
        # We are in a Bitakora Community, so catalog the post there
        cat = self.getParentNode().get('Catalog', 'None')
        if cat is not None:
            cat.catalog_object(post, '/'.join(post.getPhysicalPath()))

    self.postcount = self.postcount + 1

    if sendping:
        tech_pings = Future(sendPing, self.absolute_url(), self.blog_title())
        pingbacks = Future(postPingBacks, newbody, post.absolute_url())

    if REQUEST is not None:
        return REQUEST.RESPONSE.redirect('%s/admin?msg=%s' % (self.absolute_url(), 'Post added succesfully'))

    return newid


class Post(CatalogAware, BTreeFolder2):
    """ Post class """
    meta_type = 'Post'

    from Comment import manage_addComment
    from Reference import manage_addPingback

    security = ClassSecurityInfo()
    security.declareProtected('Add Bitakora Comment', 'manage_addComment')

    security.declareProtected('Manage Bitakora', 'edit')
    edit = HTMLFile('ui/Post_edit', globals())

    security.declarePrivate('__init__')

    def __init__(self, id, title, author, body,
                 tags=[], date=u'', publish=1, comment_allowed=1):
        """ """
        BTreeFolder2.__init__(self, id)
        self.id = str(id)
        self.title = title
        self.author = author
        self.body = body
        self.tags = tags
        self.date = date
        self.comment_allowed = comment_allowed
        self.reference_allowed = comment_allowed
        self.published = publish
        self.reindex_object()

    security.declareProtected('Manage Bitakora', 'manage_editPost')

    def manage_editPost(self, title, author, body, tags=[],
                        date=u'', publish=1, comment_allowed=1,
                        sendping=1, REQUEST=None):
        """ Editor """

        self.title = title
        self.author = author
        self.body = cleanBody(self, body)
        self.tags = prepareTags(tags)
        self.date = DateTime.DateTime(date)
        self.comment_allowed = comment_allowed
        self.reference_allowed = comment_allowed
        self.published = publish
        self.reindex_object()

        if self.inCommunity():
            # We are in a Bitakora Community, so catalog the post there
            cat = self.getParentNode().getParentNode().get('Catalog', 'None')
            if cat is not None:
                cat.catalog_object(self, '/'.join(self.getPhysicalPath()))

        if sendping:
            tech_pings = Future(sendPing,
                                self.absolute_url(),
                                self.blog_title())
            pingbacks = Future(postPingBacks,
                               self.body,
                               self.absolute_url())

        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect('%s/edit?msg=%s' % (self.absolute_url(), 'Post edited succesfully'))

    security.declareProtected('Add Bitakora Comment', 'manage_editComment')

    def manage_editComment(self, author, email, url, body,
                           date, id, publish=1, REQUEST=None):
        """ Editor """

        if REQUEST.get('delete', None):
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
        return self.posting_html(self, REQUEST)

    security.declarePublic('showTitle')

    def showTitle(self):
        """ get the title """
        return self.title

    security.declarePublic('showAuthor')

    def showAuthor(self):
        """ get the author """
        return self.author

    security.declarePublic('showTags')

    def showTags(self):
        """ get the tags """
        return u' '.join(self.tags)

    security.declarePublic('tagList')

    def tagList(self):
        """ get the tag list """
        return self.tags

    security.declarePublic('showDate')

    def showDate(self):
        """ get the date """
        return unicode(str(self.date))

    security.declarePublic('showBody')

    def showBody(self):
        """ get the body """
        return self.body

    security.declarePublic('textBody')

    def textBody(self):
        """ get the body """
        try:
            from EpozPostTidy import cleanHTML as clean
            return clean(self.body)
        except:
            # perhaps more efficient but needed for old Zopes
            # Another way... (from Zopelabs)
            intag = [False]

            def chk(c, intag):
                if intag[0]:
                    intag[0] = (c != '>')
                    return False
                elif c == '<':
                    intag[0] = True
                    return False
                return True

            return ''.join([c for c in self.body if chk(c, intag)])

    security.declarePublic('canComment')

    def canComment(self):
        """ Are the comments on this post allowed? """
        return self.comment_allowed

    security.declarePublic('canReference')

    def canReference(self):
        """ Are the references (trackbacks, pingbacks, ...)
            on this post allowed? """
        return self.reference_allowed

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
        """ get the comments of this post ordered by date"""
        if all:
            comlist = self.objectValues('Comment')[:]
        else:
            comlist = [com for com in self.objectValues('Comment') if com.published]

        comlist.sort(lambda x, y: cmp(x.date,y.date))
        return comlist

    security.declareProtected('View', 'referenceList')

    def referenceList(self, all=0):
        """ get the references of this post ordered by date """
        if all:
            reflist = self.objectValues('Reference')[:]
        else:
            reflist = [com for com in self.objectValues('Reference') if com.published]

        reflist.sort(lambda x, y:cmp(x.date,y.date))
        return reflist

    security.declarePrivate('createCommentId')

    def createCommentId(self):
        """ create id """
        l = self.commentList(all=1)
        if len(l) == 0:
            return 0
        else:
            l.sort(lambda x, y: cmp(int(x.id), int(y.id)))
            last_c_id = l[-1].getId()
            return int(last_c_id) + 1

    security.declarePrivate('createReferenceId')

    def createReferenceId(self):
        """ create id """
        if len(self.referenceList()) == 0:
            return 'r1'
        else:
            return 'r' + str(len(self.referenceList()) + 1)

    security.declareProtected('View', 'numberOfComments')

    def numberOfComments(self):
        """ Method that returns the number of comments of this post """
        return unicode(str(len(self.commentList())))

    security.declareProtected('View', 'numberOfReferences')

    def numberOfReferences(self):
        """ Method that returns the number of references of this post """
        return unicode(str(len(self.referenceList())))

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

    referencesModerated = commentsModerated

    security.declarePublic('commentsNotAllowed')

    def commentsNotAllowed(self):
        """ Are not comments allowed? """
        return not self.comment_allowed

Globals.InitializeClass(Post)
