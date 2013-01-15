# -*- coding: utf-8 -*-
# (c) Copyright 2005, CodeSyntax <http://www.codesyntax.com>
# Authors: Mikel Larreategi <mlarreategi@codesyntax.com>
# See also LICENSE.txt

from xml.sax.handler import ContentHandler
from xml.sax import make_parser


class XMLImporter(ContentHandler):

    def __init__(self):
        self.posts = []
        self.comments = []
        self.reset()

    def reset(self):
        self.inpost = 0
        self.incomment = 0
        self.incomments = 0
        self.intitle = 0
        self.inauthor = 0
        self.infmt = 0
        self.inid = 0
        self.inbody = 0
        self.intags = 0
        self.indate = 0
        self.title = ''
        self.author = ''
        self.fmt = ''
        self.body = ''
        self.tags = ''
        self.date = ''
        self.id = ''
        self.resetComment()

    def startElement(self, tag, attrs):

        if self.inpost and not self.incomment:
            if tag == 'author':
                self.inauthor = 1
            elif tag == 'body':
                self.inbody = 1
            elif tag == 'date':
                self.indate = 1
            elif tag == 'id':
                self.inid = 1

        elif self.incomment:
            if tag == 'author':
                self.incommauthor = 1
            elif tag == 'body':
                self.incommbody = 1
            elif tag == 'date':
                self.incommdate = 1

        if tag == 'post':
            self.inpost = 1
        elif tag == 'url':
            self.inurl = 1
        elif tag == 'email':
            self.inemail = 1
        elif tag == 'tags':
            self.intags = 1
        elif tag == 'fmt':
            self.infmt = 1
        elif tag == 'title':
            self.intitle = 1
        elif tag == 'comment':
            self.incomment = 1
        elif tag == 'comments':
            self.incomments = 1

    def endElement(self, tag):

        if self.inpost and not self.incomment:
            if tag == 'author':
                self.inauthor = 0
            elif tag == 'body':
                self.inbody = 0
            elif tag == 'date':
                self.indate = 0
            elif tag == 'id':
                self.inid = 0

        elif self.incomment:
            if tag == 'author':
                self.incommauthor = 0
            elif tag == 'body':
                self.incommbody = 0
            elif tag == 'date':
                self.incommdate = 0

        if tag == 'post':
            self.inpost = 0
            self.createPost()
            self.reset()
        elif tag == 'url':
            self.inurl = 0
        elif tag == 'email':
            self.inemail = 0
        elif tag == 'tags':
            self.intags = 0
        elif tag == 'fmt':
            self.infmt = 0
        elif tag == 'title':
            self.intitle = 0
        elif tag == 'comment':
            self.incomment = 0
            self.createComment()
            self.resetComment()
        elif tag == 'comments':
            self.incomments = 0

    def characters(self, chars):
        if self.intitle:
            self.title += chars
        elif self.inauthor:
            self.author += chars
        elif self.infmt:
            self.fmt += chars
        elif self.inbody:
            self.body += chars
        elif self.intags:
            self.tags += chars
        elif self.indate:
            self.date += chars
        elif self.incommauthor:
            self.commauthor += chars
        elif self.incommdate:
            self.commdate += chars
        elif self.incommbody:
            self.commbody += chars
        elif self.inurl:
            self.url += chars
        elif self.inemail:
            self.email += chars
        elif self.inid:
            self.id += chars

    def createPost(self):
        post = {}
        post['id'] = self.id
        post['title'] = self.title
        post['author'] = self.author
        post['fmt'] = self.fmt
        post['body'] = self.body
        post['tags'] = self.tags.split(';')
        post['date'] = self.date
        post['comments'] = self.comments[:]
        self.comments = []
        self.posts.append(post)

    def createComment(self):
        comment = {}
        comment['author'] = self.commauthor
        comment['date'] = self.commdate
        comment['body'] = self.commbody
        comment['url'] = self.url
        comment['email'] = self.email
        self.comments.append(comment)

    def resetComment(self):
        self.commauthor = ''
        self.commdate = ''
        self.commbody = ''
        self.url = ''
        self.email = ''
        self.incommauthor = 0
        self.incommdate = 0
        self.incommbody = 0
        self.inurl = 0
        self.inemail = 0

    def returnData(self):
        return self.posts


def importXML(xml):
    from cStringIO import StringIO
    xmlimporter = XMLImporter()
    parser = make_parser()
    parser.setContentHandler(xmlimporter)
    parser.parse(StringIO(xml))
    return xmlimporter.returnData()

if __name__ == '__main__':
    fp = open('/tmp/tolon.xml', 'r')
    print importXML(fp.read())
    fp.close()
