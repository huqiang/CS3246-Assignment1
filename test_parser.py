import sys, os
from HTMLDocument import HTMLDocument
from HTMLParser import HTMLParser

class HTMLDocumentParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.start_of_content = False
        self.contents = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'pre':
            self.start_of_content = True

    def handle_endtag(self, tag):
        if tag == 'pre':
            self.start_of_content = False        

    def handle_data(self, data):
        if self.start_of_content:
            self.contents += data

root = 'data_project1/'

for root, dirnames, filenames in os.walk(root):
    for filename in filenames:
        file = open(root + filename)
        contents = unicode(file.read(), 'iso-8859-1')
        doc_parser = HTMLDocumentParser()
        doc_parser.feed(contents)
        html_doc = HTMLDocument(doc_parser.contents)
        # print html_doc.contents_array
        print filename + ': '
        print '=============='
        print 'Title: ' + html_doc.title
        print 'Description: ' + html_doc.description
        print 'Month: ' + html_doc.month
        print 'Year: ' + html_doc.year
        print 'Authors: ' + str(html_doc.authors)
        print 'Keywords: ' + str(html_doc.keywords)
        print 'Timestamp: ' + str(html_doc.timestamp)
        print ' '
        file.close()

# file = open(root + '2144.html')
# contents = unicode(file.read(), 'iso-8859-1')
# doc_parser = HTMLDocumentParser()
# doc_parser.feed(contents)
# html_doc = HTMLDocument(doc_parser.contents)
# print html_doc.contents_array
# print html_doc.title
# print ' '
# file.close()