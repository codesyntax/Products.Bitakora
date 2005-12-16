###
# EpozPostTidy.py
#
# This is just an example for transforming
# absolute urls to relative urls with Epoz.
#
# Use it at your own risk or improve it!
###

from Products.Bitakora.HTMLParser import HTMLParser
import re

# These tags will get a newline after the closing tag
blocktags = ['p', 'pre', 'div',
             'table', 'tr', 'th', 'td', 'thead', 'tbody', 'tfoot',
             'ul','ol','li',
             'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
             
allowedtags = ['p', 'pre', 'table', 'tr', 'th', 'td', 'thead', 'tbody', 'tfoot',
             'ul','ol','li','h3', 'h4', 'h5', 'h6', 'blockquote', 'q', 'cite', 'b', 'i',
             'strong', 'em', 'a', 'iframe']
             
replaceabletags = {'b':'strong', 'i':'em'}             

allowedattrs = ['href', 'src', 'alt', 'title']             

# Just a simple htmlparser
class aHTMLParser(HTMLParser):
    res = u""

    def handle_starttag(self, tag, attrs):
        if tag in ['br', 'hr', 'img']:
            self.handle_startendtag(tag, attrs)
        elif tag in allowedtags:
            attributes= u""
            for (key,value) in attrs:
                # Internal Link?
                """
                if (tag=="a" and key=="href"):
                    value = self.getRelativeUrl(self.pageurl, value)                   
                """
                if key in allowedattrs:
                    attributes += u' %s="%s"' % (key,value)

            if tag in replaceabletags.keys():
                self.res += u"<%s%s>" % (replaceabletags[tag], attributes)
            else:
                self.res += u"<%s%s>" % (tag, attributes)

    def handle_endtag(self, tag):
        if tag in allowedtags:
            if tag in replaceabletags.keys():
                self.res += u"</%s>" % (replaceabletags[tag],)
            else:
                self.res += u"</%s>" % (tag,)
            # Some pretty-nice-printing for block-elements
            if tag in blocktags:
                self.res += u"\n"

    def handle_startendtag(self, tag, attrs):
        attributes= u""
        for (key,value) in attrs:
            # Image?
            """
            if tag=="img" and key=="src":
                value = self.getRelativeUrl(self.pageurl, value)
            """                
            attributes += u' %s="%s"' % (key,value)
        self.res += u"<%s%s />" % (tag, attributes)

    def handle_data(self, data):
        self.res += data

    def handle_charref(self, data):
        self.res += u"&%s;" % data

    def handle_entityref(self, data):
        self.res += u"&%s;" % data

    def handle_comment(self, data):
        pass
        #self.res += "<!-- %s -->"

class cleanHTMLParser(HTMLParser):
    res = u''
    
    def handle_startag(self, tag, attrs):
        if tag in ['br', 'hr', 'img']:
            self.handle_startendtag(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        return
        
    def handle_endtag(self, tag):
        return
        
    def handle_data(self, data):
        self.res += data
        
    def handle_charref(self, data):
        self.res += u"&%s;" % data

    def handle_entityref(self, data):
        self.res += u"&%s;" % data

    def handle_comment(self, data):
        pass



def EpozPostTidy(self, html, pageurl):
    # Create a parser
    parser = aHTMLParser()

    # Give the parser the global method for relative urls
    parser.getRelativeUrl = self.EpozGetRelativeUrl

    # Submit the pageurl as base-url for calculating urls
    parser.pageurl = pageurl

    # And now lets turn the wheels
    parser.feed(html)
    parser.close()

    # Get & return postprocessed html from parser
    html = parser.res

    # Just some cleanups to remove useless whitespace
    html = re.sub("[ ]+"," ",html)
    html = re.sub("[\n]+","\n", html)
    
    return html
    
def cleanHTML(html):
    parser = cleanHTMLParser()
    parser.feed(html)
    parser.close()
    htmlres = parser.res   
    htmlres = re.sub("[ ]+"," ",htmlres)
    htmlres = re.sub("[\n]+","\n", htmlres)
    
    return htmlres
