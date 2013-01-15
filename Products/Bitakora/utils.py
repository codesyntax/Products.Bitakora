# -*- coding: utf-8 -*-
# (c) Copyright 2005, CodeSyntax <http://www.codesyntax.com>
# Authors: Mikel Larreategi <mlarreategi@codesyntax.com>
#
# Portions Copyright (c) 2000-2001 Chris Withers
#
# See also LICENSE.txt

# Importing
from Products.PythonScripts.PythonScript import manage_addPythonScript
from Products.PythonScripts.standard import url_quote

import Globals

import string
try:
    import urllib2 as urllib
except:
    import urllib
import re, os
import xmlrpclib
from urllister import URLLister

ok_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_ '
CAPTCHAS_NET_USER = 'bitakora'
CAPTCHAS_NET_SECRET = 'HmE2OawsnKWxzHpgQRNmW9RuR5Ea8zV2Sn5eRzrT'
AKISMET_KEY = '5cbed64f50bb'
AKISMET_AGENT = 'Bitakora [http://www.codesyntax.com/bitakora]'
AKISMET_ENABLED = 0
PARSE_ENABLED = POST_PARSE_ENABLED = 0
COMMENT_PARSE_ENABLED = 1
# Many of these methods have been copied and personalized
# from Squishdot, COREBlog and CPS


def addDTML(obj, id, title, file):
    file_path = Globals.package_home(globals())
    f = open(file_path + '/' + file + '.dtml')
    file = f.read()
    f.close()
    obj.manage_addDTMLMethod(id, title, file)
    return getattr(obj, id)


def addPythonScript(obj, id, file):
    file_path = Globals.package_home(globals())
    f = open(file_path + '/' + file + '.py')
    file = f.read()
    f.close()
    manage_addPythonScript(obj, id)
    obj._getOb(id).write(file)
    return getattr(obj, id)


def addImage(obj, id, file):
    file_path = Globals.package_home(globals())
    f = open(file_path + '/' + file, 'rb')
    contents = f.read()
    f.close()
    title = ''
    obj.manage_addImage(id, contents, title=title)


def addFile(obj, id, file):
    file_path = Globals.package_home(globals())
    f = open(file_path + '/' + file, 'rb')
    contents = f.read()
    f.close()
    title = ''
    obj.manage_addFile(id, contents, title=title)


def clean(text):
    """ clean the text to delete all unwanted things """
    return text


def cleanCommentBody(self, text):
    """ clean the text to delete all unwanted HTML """
    if not COMMENT_PARSE_ENABLED:
        return text

    try:
        from EpozPostTidy import EpozPostTidy
    except:
        def EpozPostTidy(self, text, s=''):
            return text

    return EpozPostTidy(self, text, '')


def cleanBody(self, text):
    """ clean the text to delete all unwanted HTML """
    if not POST_PARSE_ENABLED:
        return text

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

    sep = '!"#$%&\'()*+,./:;<=>?@[\\]^`{|}~'
    mt = string.maketrans(unicode(sep), unicode(' ' * (len(sep))))
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


def send_contact_mail(context, name=u'', email=u'',
                      subject=u'', body=u'', bitakora_cpt='',
                      random_cpt='', captcha_zz=0, REQUEST=None):
    """ Send a mail to blog owner """
    if not checkNewCaptchaValue(context, bitakora_cpt):
        if REQUEST is not None:
            return REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER.split('?')[0]+'?msg=%s&name=%s&email=%s&subject=%s&body=%s#bitakora_cpt_control' % (context.gettext('Are you a bot? Please try again...'), url_quote(name.encode('utf-8')), url_quote(email.encode('utf-8')), url_quote(subject.encode('utf-8')), url_quote(body.encode('utf-8'))))

        return None

    try:
        mailhost = context.MailHost
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

        variables = {}
        variables['from'] = mFrom.encode('utf-8')
        variables['to'] = mTo.encode('utf-8')
        variables['comment_author'] = name.encode('utf-8')
        variables['comment_email'] = email.encode('utf-8')
        variables['comment_subject'] = subject.encode('utf-8')
        variables['comment_body'] = body.encode('utf-8')
        mSubj = context.gettext('New message from your blog!')
        mMsg = context.contact_email_template(context, **variables)
        notifyByEmail(mailhost, mTo.encode('utf-8'),
                      mFrom.encode('utf-8'), mSubj.encode('utf-8'),
                      mMsg.encode('utf-8'))
    except Exception, e:
        # If there is no MailHost, or other error happened
        # there won't be e-mail notifications
        from logging import getLogger
        log = getLogger('send_contact_mail')
        log.info(e)

    if REQUEST is not None:
        return REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER.split('?')[0] + '?msg=Ok')


def fillMessageCatalog(gettext):
    locales = ['eu', 'es', 'pl']
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
    if headers.get('x-pingback', None):
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
        return """ Ezin da: %s, %s, %s""" % (sourceURI, targetURI, serverURI)
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


def getCaptchaImage(self):
    """ Get a captcha image from Captchas.net service,
        using bitakora's user and password"""
    from CaptchasDotNet import CaptchasDotNet

    captcha = CaptchasDotNet(client=CAPTCHAS_NET_USER,
                             secret=CAPTCHAS_NET_SECRET)

    rnd = captcha.random()
    img = captcha.image()

    return rnd, img


def checkCaptchaValue(random, input):
    """ Check the captcha using Captchas.net service """
    from CaptchasDotNet import CaptchasDotNet

    captcha = CaptchasDotNet(client=CAPTCHAS_NET_USER,
              secret=CAPTCHAS_NET_SECRET)
    return captcha.verify(input, random)


def isCommentSpam(comment_body='', comment_author='',
                  comment_email='', comment_url='',
                  blogurl='', REQUEST=None):

    if not AKISMET_ENABLED:
        return 0

    from akismet import Akismet, AkismetError, APIKeyError
    from urllib2 import URLError, HTTPError
    from socket import timeout
    ak = Akismet(key=AKISMET_KEY, blog_url=blogurl, agent=AKISMET_AGENT)
    data = {}
    data['blog'] = blogurl
    try:
        data['user_ip'] = REQUEST.get('REMOTE_ADDR', '')
        data['user_agent'] = REQUEST.get('HTTP_USER_AGENT', '')
        data['referrer'] = REQUEST.get('HTTP_REFERER', 'unknown')
    except:
        data['user_ip'] = '192.168.0.1'
        data['user_agent'] = 'Mozilla'
        data['referrer'] = 'unknown'

    data['comment_type'] = 'comment'
    data['comment_author'] = comment_author
    data['comment_author_email'] = comment_email
    data['comment_author_url'] = comment_url

    from zLOG import LOG, INFO
    try:
        return ak.comment_check(comment=comment_body.encode('utf-8'),
                                data=data)
    except AkismetError:
        # Something happened with an argument
        LOG('isCommentSpam', INFO, 'Argument error')
        return 0
    except URLError, HTTPError:
        # Something happended with the conection
        LOG('isCommentSpam', INFO, 'Connection error')
        return 0
    except APIKeyError:
        # Something happened with the API Key
        LOG('isCommentSpam', INFO, 'APIKeyError')
        return 0
    except timeout:
        # Aghhhh, connection time out
        LOG('isCommentSpam', INFO, 'Connection timeout')
        return 0
    except Exception, e:
        # What the hell happened?
        LOG('isCommentSpam', INFO, 'Unknown error: %s' % e)

        return 0


def isPingbackSpam(title='', url='', excerpt='', blogurl='', REQUEST=None):
    if not AKISMET_ENABLED:
        return 0

    from akismet import Akismet
    ak = Akismet(key=AKISMET_KEY, blog_url=blogurl, agent=AKISMET_AGENT)
    data = {}
    data['blog'] = blogurl
    try:
        data['user_ip'] = REQUEST.get('REMOTE_ADDR', '')
        data['user_agent'] = REQUEST.get('HTTP_USER_AGENT', '')
        data['referrer'] = REQUEST.get('HTTP_REFERER', 'unknown')
    except:
        pass

    data['comment_type'] = 'pingback'
    data['comment_author'] = title
    data['comment_author_email'] = url
    data['comment_author_url'] = url

    return ak.comment_check(comment=excerpt, data=data)


def sendPing(blog_url, blog_title):
    """ send Update notifications for PING Servers """
    ret_l = []
    ping_servers = ['http://rpc.technorati.com/rpc/ping']
    for pingurl in ping_servers:
        try:
            resp = send_ping(pingurl, blog_title, blog_url)
        except Exception, e:
            resp = {}
            resp["message"] = str(e)
            ret_l.append({"url": pingurl, "message": resp["message"]})

    return ret_l


def send_ping(serverurl, blogtitle, url):
    """ Make the XML RPC call with the ping """
    from xmlrpclib import Server
    version_str = 'Bitakora 0.1'
    title = blogtitle.encode('utf-8')
    svr = Server(serverurl)
    svr.Transport.user_agent = version_str
    resp = svr.weblogUpdates.ping(title, url)
    return resp


def postPingBacks(newbody, post_url):
    """ Make the pingback call """
    pingbackresults = []
    parser = URLLister()
    parser.feed(newbody)
    parser.close()
    urls = parser.urls
    for url in urls:
        url = str(url)
        result = sendPingback(url, post_url)
        pingbackresults.append((url, result))

    return pingbackresults


def sendPingback(url, self_url):
    """ Pingback making call """
    pburl = discoverPingbackUrl(url)
    if pburl is not None:
        code = makeXMLRPCCall(serverURI=pburl,
                              sourceURI=self_url,
                              targetURI=url)
        return code
    else:
        # No pingback is possible
        return 2


def getCaptchaQuestion(self):
    """ get captcha question from a property """
    try:
        return self.CAPTCHA_QUESTION
    except:
        return ''


def checkNewCaptchaValue(self, input):
    """ check the form input with the value of a property """
    try:
        return input == self.CAPTCHA_ANSWER
    except:
        return False
