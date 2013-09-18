from HTMLParser import HTMLParser

class QueryFileParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.start_of_query_number = False
        self.start_of_content      = False
        self.contents              = dict()
        self.query_number          = ''

    def handle_starttag(self, tag, attrs):
        # if tag == 'DOC':
            # self.start_of_content = True
        print tag
        if tag == 'DOCNO':
            print tag
            self.start_of_query_number = True

    def handle_endtag(self, tag):
        if tag == 'DOCNO':
            self.start_of_query_number = False        
            self.start_of_content = True
        if tag == 'DOC':
            self.start_of_content = False
    def handle_data(self, data):
        if self.start_of_query_number:
            self.query_number = data
        if self.start_of_content:
            self.contents[self.query_number]=data