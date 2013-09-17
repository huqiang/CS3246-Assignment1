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
"""
"""


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

        t1 = FieldType()
        t1.setIndexed(True)
        t1.setStored(True)
        t1.setTokenized(False)
        t1.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)
        
        t2 = FieldType()
        t2.setIndexed(True)
        t2.setStored(False)
        t2.setTokenized(True)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
        
        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                print "adding", filename
                try:
                    path     = os.path.join(root, filename)
                    file     = open(path)
                    contents = unicode(file.read(), 'iso-8859-1')
                    file.close()
                    doc      = Document()
                    doc.add(Field("name", filename, t1))
                    doc.add(Field("path", root, t1))
                    if len(contents) > 0:
                        doc.add(Field("contents", contents, t2))
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
