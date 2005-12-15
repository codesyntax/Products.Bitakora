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

__version__ = "$Revision: 0.01 $"

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
            return '0'
        elif not self.exists(sourceURI):
            return '0x0010'
        elif not self.hasLinkToTarget(sourceURI, targetURI):
            return '0x00110'
        elif not self.targetExists(targetURI):
            return '0x0020'
        elif not self.pingable(targetURI):
            return '0x0021'
        elif self.pingbackExists(sourceURI, targetURI):
            return '0x0030'
        else:
            # Everything seems to be OK now :)
            sock = urllib.urlopen(sourceURI)
            html = sock.read()
            sock.close()
            post = self.pingable(targetURI)
            excerpt = self.extractExcerpt(targetURI, html)
            title = self.extractTitle(html)
            post.manage_addPingback(title, sourceURI, excerpt)
            return '200 OK'

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
        # pieces = ['http:', '', 'www.eibar.com', 'blogak', 'mikel', 'asdfasdfaf']
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
            post = getattr(blog, postId)
            if post and post.canReference():
                return post
            else:
                return 0
        except:
            # Hau ez da post bat...
            pass

    security.declarePrivate('targetExists')
    def targetExists(self, targetURI):
        return 1

    security.declarePrivate('pingbackExists')
    def pingbackExists(self, sourceURI, targetURI):
        post = self.pingable(targetURI)
        if post.hasPingback(sourceURI):
            return 1
        else:
            return 0

    security.declarePrivate('fetchSource')
    def fetchSource(self, sourceURI):
        return ''

    security.declarePrivate('extractExcerpt')
    def extractExcerpt(self, targetURI, html):
        pos = html.find(targetURI)
        start = pos - 150
        end = pos + 150
        excerpt = html[start:end]
        return unicode('...'+excerpt+'...')

    security.declarePrivate('extractTitle')
    def extractTitle(self, html):
        import re
        reg = re.compile('<title>([^<]*?)</title>', re.I)
        matches = reg.search(html)
        titles = matches.groups()
        return titles[0]
