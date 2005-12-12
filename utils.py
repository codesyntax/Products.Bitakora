# Importing
from Products.PythonScripts.PythonScript import manage_addPythonScript

import Globals

import string
try:
    import urllib2 as urllib
except:
    import urllib
import re
import xmlrpclib

ok_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_ '

# Many of these methods have been copied and personalized from Squishdot, COREBlog and CPS


def addDTML(obj,id,title,file): 
    file_path = Globals.package_home(globals())
    f=open(file_path+'/'+file+'.dtml')
    file=f.read()
    f.close()
    obj.manage_addDTMLMethod(id,title,file)
    return getattr(obj,id)

def addPythonScript(obj,id,file):
    file_path = Globals.package_home(globals())
    f=open(file_path+'/'+file+'.py')     
    file=f.read()
    f.close()     
    manage_addPythonScript(obj,id)
    obj._getOb(id).write(file)
    return getattr(obj,id)    

def addImage(obj,id,file):     
    file_path = Globals.package_home(globals())
    f=open(file_path+'/'+file,'rb')     
    contents=f.read()     
    f.close()     
    title=''     
    tlen = len(contents)     
    new_id = obj.manage_addImage(id,contents,title=title)   
    
        
def createUploadable(filename):
    file_path = Globals.package_home(globals())
    filename=file_path+'/'+filename
    f=open(filename,'rb')
    # extra step 'cos we can't set attributes on files
    s=StringIO(f.read())
    s.filename=filename
    return s
    
def addFile(obj,id,file):
    file_path = Globals.package_home(globals())
    f=open(file_path+'/'+file,'rb')           
    contents=f.read()     
    f.close()     
    title=''     
    tlen = len(contents)     
    new_id = obj.manage_addFile(id,contents,title=title)   

def createId(title):
    """ Create an id for a post based on its title """
    id = title.strip()
    #id = tit.translate(translation_table)
    id = ''.join([c for c in id if c in ok_chars])
    while id.startswith('-') or id.startswith('_') or id.startswith(' '):
        id = id[1:]

    while id.endswith('-') or id.endswith('_') or id.endswith(' '):
        id = id[:-1]

    id = id.lower()
    if not id:
        return u'blog-post%d' % self.postcount

    return u'-'.join(id.split(' '))

def createNewId(oldid):
    """ Create a new id if the previous one was taken """
    if oldid[-1].isdigit():
        num = oldid.split('-')
        end = int(num[-1]) + 1
        return '-'.join(num[:-1]) + '-' + str(end)
    else:
        return oldid+'-1'

def clean(text):
    """ clean the text to delete all unwanted things """
    return text

def cleanBody(self, text):
    """ clean the text to delete all unwanted HTML """
    from EpozPostTidy import EpozPostTidy
    
    return EpozPostTidy(self, text, '')

def prepareTags(tags=[]):
    """ prepare the tags deleting all unwanted things """
    return tags
    import string
    
    mt = string.maketrans(string.punctuation, ' '*(len(string.punctuation)))
    
    newtags = []
    for tag in tags:
        t = tag.encode('utf-8')
        t = t.translate(mt)
        t = t.strip()
        t = unicode(t)
        t = t.lower()
        newtags.append(t)
        
    return newtags


def cleanEmail(email):
    """ clean email """
    return email

def cleanURL(url):
    """ clean url """
    return url

def discoverPingbackUrl(url):
    """ There are 2 ways to discover the pingback URL of a given URL:
        1- The server sends a HTTP Header X-Pingback: url with the url to ping
        2- The HTML of the targetURI has a special <link> tag with the url

        More info: http://www.hixie.ch/specs/pingback/pingback
    """
    try:
        sock = urllib.urlopen(url)
    except:
        return None
    headers = sock.headers
    if headers.has_key('x-pingback'):
        # fine ! we have a HTTP HEADER with the pingback URL :)
        return headers.get('x-pingback')
    else:
        # ups, we must find out in the HTML code
        # looking for a proper <link> tag :(
        html = sock.read()
        reg = re.compile('<link rel="pingback" href="([^"]+)" ?/?>')
        matches = reg.search(html)
        if matches:
            pbs = matches.groups()
            if len(pbs) > 0:
                # Good ! We have a pingback URL ...
                return pbs[0]
            else:
                # Ups, no pingback url available :(
                return None
        else:
            return None

def makeXMLRPCCall(serverURI, sourceURI, targetURI):
    server = xmlrpclib.Server(serverURI)
    try:
        res = server.pingback.ping(sourceURI, targetURI)
    except:
        return """ Ezin da """
    if res == '0':
        return """ A generic fault code. Servers MAY use this error code instead of any of the others if they do not have a way of determining the correct fault code."""

    elif res == '0x0010':
        return """ The source URI does not exist """

    elif res == '0x00110':
        return """ The source URI does not contain a link to the target URI, and so cannot be used as a source """
    elif res == '0x0020':
        return """ The specified target URI does not exist. This MUST only be used when the target definitely does not exist, rather than when the target may exist but is not recognised. """

    elif res == '0x0021':
        return """     The specified target URI cannot be used as a target. It either doesn't exist, or it is not a pingback-enabled resource. For example, on a blog, typically only permalinks are pingback-enabled, and trying to pingback the home page, or a set of posts, will fail with this error. """
    elif res == '0x0030':
        return """ The pingback has already been registered. """

    elif res == '0x00310':
        return """ Access denied. """

    elif res == '0x0032':
        return """ The server could not communicate with an upstream server, or received an error from an upstream server, and therefore could not complete the request. This is similar to HTTP's 402 Bad Gateway error. This error SHOULD be used by pingback proxies when propagating errors. """

    else:
        return res