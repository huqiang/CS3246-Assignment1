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