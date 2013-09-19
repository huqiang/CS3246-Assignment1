#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time
from datetime import datetime

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
import org.apache.lucene.search.similarities as similarities

from HTMLDocument import HTMLDocument
from HTMLDocumentParser import HTMLDocumentParser

class Indexer(object):
    """Usage:   python IndexFiles <doc_directory>
    """

    def __init__(self, fileRoot, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store    = SimpleFSDirectory(File(storeDir))
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config   = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setSimilarity(similarities.BM25Similarity())
    #Available similarity: BM25Similarity, MultiSimilarity, PerFieldSimilarityWrapper, SimilarityBase, TFIDFSimilarity
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer   = IndexWriter(store, config)

        self.indexDocs(fileRoot, writer)
        print 'commit index',
        writer.commit()
        writer.close()
        print 'done'

    def indexDocs(self, root, writer):

        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                print "adding", filename
                doc_parser = HTMLDocumentParser()
                try:
                    path = os.path.join(root, filename)
                    file = open(path)
                    contents = unicode(file.read(), 'iso-8859-1')
                    doc_parser.feed(contents)
                    html_doc = HTMLDocument(doc_parser.contents)

                    flag = False
                    if flag:
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

                    doc = Document()

                    field_filename = FieldType()
                    field_filename.setIndexed(True)
                    field_filename.setStored(True)
                    field_filename.setTokenized(False)
                    field_filename.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)        
                    doc.add(Field("filename", filename.replace('.html', ''), field_filename))

                    field_path = FieldType()
                    field_path.setIndexed(True)
                    field_path.setStored(True)
                    field_path.setTokenized(True)
                    field_path.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
                    doc.add(Field("path", root, field_path))
                    
                    field_title = FieldType()
                    field_title.setIndexed(True)
                    field_title.setStored(True)
                    field_title.setTokenized(True)
                    field_title.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)        
                    doc.add(Field("title", html_doc.title, field_title))

                    
                    field_description = FieldType()
                    if html_doc.has_description():
                        field_description.setIndexed(True)
                    else:
                        field_description.setIndexed(True)
                    field_description.setStored(True)
                    field_description.setTokenized(True)
                    field_description.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)        
                    doc.add(Field("description", html_doc.description, field_description))

                    field_month = FieldType()
                    field_month.setIndexed(True)
                    field_month.setStored(True)
                    field_month.setTokenized(False)
                    field_month.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)        
                    doc.add(Field("month", html_doc.month, field_month))

                    field_year = FieldType()
                    field_year.setIndexed(True)
                    field_year.setStored(True)
                    field_year.setTokenized(False)
                    field_year.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)        
                    doc.add(Field("year", html_doc.year, field_year))

                    if html_doc.has_authors():
                        field_author = FieldType()
                        field_author.setIndexed(True)
                        field_author.setStored(True)
                        field_author.setTokenized(True)
                        field_author.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS) 
                        for author in html_doc.authors:
                            doc.add(Field("author", author, field_author))

                    if html_doc.has_keywords():
                        field_keyword = FieldType()
                        field_keyword.setIndexed(True)
                        field_keyword.setStored(True)
                        field_keyword.setTokenized(True)
                        field_keyword.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS) 
                        for keyword in html_doc.keywords:
                            doc.add(Field("keyword", keyword, field_keyword))

                    field_timestamp = FieldType()
                    field_timestamp.setIndexed(False)
                    field_timestamp.setStored(True)
                    field_timestamp.setTokenized(False)
                    field_timestamp.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)        
                    doc.add(Field("timestamp", html_doc.timestamp, field_timestamp))

                    if len(contents) > 0:
                        field_source = FieldType()
                        field_source.setIndexed(True)
                        field_source.setStored(False)
                        field_source.setTokenized(True)
                        field_source.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS) 
                        doc.add(Field("contents", contents, field_source))
                    else:
                        print "warning: no content in %s" % filename
                    writer.addDocument(doc)
                except Exception, e:
                    print "Failed in indexDocs:", e

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print IndexFiles.__doc__
        sys.exit(1)
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    try:
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        Indexer(sys.argv[1], os.path.join(base_dir, INDEX_DIR),
                   StandardAnalyzer(Version.LUCENE_CURRENT))
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
        raise e
