# -*- coding: utf-8 -*-
# (c) Copyright 2005, CodeSyntax <http://www.codesyntax.com>
# Authors: Mikel Larreategi <mlarreategi@codesyntax.com>
# See also LICENSE.txt

#$Id$

# Zope modules
from OFS.SimpleItem import SimpleItem
from OFS.Traversable import Traversable
from Acquisition import Implicit
from AccessControl import ClassSecurityInfo
from Globals import Persistent

try:
    import urllib2 as urllib
except:
    import urllib

from urllister import URLLister

from logging import getLogger
log = getLogger('PingMethodContainer')

class PingMethodContainer(Persistent, SimpleItem, Implicit, Traversable):
    """ An object to provide 'ping' method for pingbacks  """

    meta_type = 'PingbackObject'
    security = ClassSecurityInfo()

    security.declarePrivate('__init__')

    def __init__(self):
        """Some stuff here"""
        self.id = 'pingback'

    __call__ = None
    index_html = None

    security.declarePublic('getId')

    def getId(self):
        return self.id

    security.declarePublic('ping')

    def ping(self, sourceURI='', targetURI=''):
        """ some stuff here too """
        if not sourceURI or not targetURI or \
           not sourceURI.startswith('http') or not targetURI.startswith('http'):
            log.info('not valid URIs: tgt %s src %s' % (targetURI, sourceURI))
            return '0'
        if not self.exists(sourceURI):
            log.info('source does not exist: %s' % sourceURI)
            return '0x0010'
        if not self.hasLinkToTarget(sourceURI, targetURI):
            log.info('source does not have link to target src %s tg %s' % (sourceURI, targetURI))
            return '0x00110'
        if not self.targetExists(targetURI):
            log.info('target does not exist: %s' % targetURI)
            return '0x0020'
        if not self.pingable(targetURI):
            log.info('target is not pingable: %s' % targetURI)
            return '0x0021'
        if self.pingbackExists(sourceURI, targetURI):
            log.info('pingback already exists target src %s tg %s' % (sourceURI, targetURI))
            return '0x0030'

        # Everything seems to be OK now :)
        sock = urllib.urlopen(sourceURI)
        html = sock.read()
        sock.close()
        excerpt = self.extractExcerpt(targetURI, html)
        title = self.extractTitle(html)
        post = self.getPostFromURI(targetURI)
        post.manage_addPingback(title, sourceURI, excerpt)
        return 1

    security.declarePrivate('exists')

    def exists(self, sourceURI):
        try:
            sock = urllib.urlopen(sourceURI)
            html = sock.read()
            return 1
        except:
            return 0

    security.declarePrivate('hasLinkToTarget')

    def hasLinkToTarget(self, sourceURI, targetURI):
        sock = urllib.urlopen(sourceURI)
        html = sock.read()
        sock.close()
        # use Mark Pilgrim's URLLister from dive into python, chapter 8
        parser = URLLister()
        parser.feed(html)
        parser.close()

        links = parser.urls
        if targetURI in links:
            return 1
        else:
            return 0

    security.declarePrivate('pingable')

    def pingable(self, targetURI):
        # targetURI = http://www.eibar.com/blogak/mikel/asdfasdfaf
        pieces = targetURI.split('/')
        if pieces[-1] == '':
            # the URI was http://www.eibar.com/blogak/mikel/asdfasdfaf/
            postId = pieces[-2]
        else:
            postId = pieces[-1]

        if postId.find('#') != -1:
            # ups, it's a comment's URL
            return 0
        # Acquisition.Implicit -i esker gurasoen metodoetan bilatzen du
        blog = self.blog()
        try:
            post = getattr(blog, postId, None)
            if post is not None and post.canReference():
                return 1
            else:
                return 0
        except:
            # Hau ez da post bat...
            return 0

    security.declarePrivate('targetExists')

    def targetExists(self, targetURI):
        try:
            sock = urllib.urlopen(targetURI)
            sock.close()
            return 1
        except:
            return 0

    security.declarePrivate('getPostFromURI')

    def getPostFromURI(self, uri):
        pieces = uri.split('/')
        postId = ''
        if pieces[-1] == '':
            # the URI was http://www.eibar.com/blogak/mikel/asdfasdfaf/
            postId = pieces[-2]
        else:
            postId = pieces[-1]

        if postId.find('#') != -1:
            # ups, it's a comment's URL
            return 0
        # Acquisition.Implicit -i esker gurasoen metodoetan bilatzen du
        blog = self.blog()
        post = blog.get(postId, None)
        return post

    security.declarePrivate('pingbackExists')

    def pingbackExists(self, sourceURI, targetURI):
        post = self.getPostFromURI(targetURI)
        if post is not None and post.hasPingback(sourceURI):
            return 1
        else:
            return 0

    security.declarePrivate('extractExcerpt')

    def extractExcerpt(self, targetURI, html):
        from EpozPostTidy import pingbackHTML
        cleanedhtml = pingbackHTML(html)
        pos = cleanedhtml.find(targetURI)
        start = pos - 150
        end = pos + 150
        excerpt = cleanedhtml[start:end]

        return unicode('...' + excerpt + '...')

    security.declarePrivate('extractTitle')

    def extractTitle(self, html):
        import re
        reg = re.compile('<title>([^<]*?)</title>', re.I)
        matches = reg.search(html)
        titles = matches.groups()
        return titles[0]
