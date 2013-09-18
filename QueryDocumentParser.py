from HTMLParser import HTMLParser

class QueryDocumentParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.query_content_started = False
        self.query_started = False
        self.contents = []
        self.current_query_num = ''
        self.current_query = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'doc':
            self.query_content_started = True
        elif tag == 'docno' and self.query_content_started:
            self.query_started = True

    def handle_endtag(self, tag):
        if tag == 'doc':
            self.query_content_started = False
        elif tag == 'docno':
            self.query_started = False

    def handle_data(self, data):
        if self.query_content_started:
            if self.query_started:
                self.current_query_num = data
            elif self.current_query_num and len(self.current_query_num) != 0:
                self.contents.append({'query_no': self.current_query_num.strip(), 'query_content': data.replace('\r', '').replace('\n', ' ').strip()})
                self.current_query_num = ''
                self.current_query = ''