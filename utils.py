# -*- coding: utf-8 -*-
# (c) Copyright 2005, CodeSyntax <http://www.codesyntax.com>
# Authors: Mikel Larreategi <mlarreategi@codesyntax.com>
#
# Portions Copyright (c) 2000-2001 Chris Withers
#
# See also LICENSE.txt

#$Id$

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
      
def addFile(obj,id,file):
    file_path = Globals.package_home(globals())
    f=open(file_path+'/'+file,'rb')           
    contents=f.read()     
    f.close()     
    title=''     
    tlen = len(contents)     
    new_id = obj.manage_addFile(id,contents,title=title)   

def clean(text):
    """ clean the text to delete all unwanted things """
    return text

def cleanBody(self, text):
    """ clean the text to delete all unwanted HTML """
    try:
        from EpozPostTidy import EpozPostTidy
    except:
        def EpozPostTidy(self, text, s=''):
            return text
    
    return EpozPostTidy(self, text, '')

def prepareTags(tags=[]):
    """ prepare the tags deleting all unwanted things """
    try:
        from sets import Set as set    
    except:
        def set(li):
            return li
            
    import string
    
    sep = '!"#$%&\'()*+,./:;<=>?@[\\]^`{|}~'
    mt = string.maketrans(unicode(sep), unicode(' '*(len(sep))))
    mt = unicode(mt, 'iso-8859-1')
    newtags = []
    for tag in tags:
        t = tag
        t = t.translate(mt)
        t = t.strip()
        #t = unicode(t)
        t = t.lower()
        if t:
            newtags.append(t)

    return list(set(newtags))

def cleanEmail(email):
    """ clean email """
    return email

def cleanURL(url):
    """ clean url """
    return url


def notifyByEmail(mailhost, mTo, mFrom, mSubj, mMsg):
    mailhost.send(mMsg, mTo, mFrom, mSubj)


def send_contact_mail(context, name=u'', email=u'', subject=u'', body=u''):
    try:
        mailhost = getattr(context,context.superValues('Mail Host')[0].id)
        try:
            from EpozPostTidy import cleanHTML
        except ImportError:
            def cleanHTML(text):
                return text
        
        mTo = context.contact_mail
        if context.inCommunity():
            mFrom = context.admin_mail
        else:
            mFrom = context.contact_mail
        mSubj = context.gettext('New message from your blog!') 
        mMsg = context.gettext("""To: %s
From: %s
Mime-Version: 1.0
Content-Type: text/plain; charset=UTF-8

Comment author :%s
Author's email :%s
Comment subject:%s
Comment body   :
%s
    
""") % (mTo.encode('utf-8'), mFrom.encode('utf-8'), name.encode('utf-8'), email.encode('utf-8'), subject.encode('utf-8'), cleanHTML(body).encode('utf-8'))
    
        notifyByEmail(mailhost, mTo.encode('utf-8'), mFrom.encode('utf-8'), mSubj.encode('utf-8'), mMsg)    
    except:
        # If there is no MailHost, or other error happened
        # there won't be e-mail notifications
        pass


def fillMessageCatalog(gettext):
    locales = ['eu', 'es']
    file_path = Globals.package_home(globals())
    log = []
    for locale in locales:
        fp = open('%s/locale/%s.po' % (file_path, locale))
        try:
            gettext.po_import(locale, fp.read())
        except:
            log.append('Locale %s could not be imported')
        fp.close()
        
    if log:
        return log

    return 1

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
    res = ''
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