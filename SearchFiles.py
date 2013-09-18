#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
import org.apache.lucene.search.similarities as similarities

import QueryFileParser

"""

"""
def run(searcher, analyzer):
    while True:
        print
        print "Hit enter with no input to quit."
        command = raw_input("Query:")
        if command == '':
            return

        print
        print "Searching for:", command
        query = QueryParser(Version.LUCENE_CURRENT, "contents",
                            analyzer).parse(command)
        scoreDocs = searcher.search(query, 10).scoreDocs
        print "%s total matching documents." % len(scoreDocs)

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print 'path:', doc.get("path"), 'name:', doc.get("name"), scoreDoc.score


def search_query_from_file(searcher, analyzer, query_file):
    queries = QueryFileParser.parse_query_file(query_file)
    for Q in queries:
        print Q['query_no'],"  ", Q['query_content']
        query = QueryParser(Version.LUCENE_CURRENT, "contents",
                            analyzer).parse(Q['query_content'])
        scoreDocs = searcher.search(query, 10).scoreDocs
        print "%s total matching documents." % len(scoreDocs)

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print Q['query_no'],'\t', doc.get("name"), "\t", scoreDoc.score

if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(os.path.join(base_dir, INDEX_DIR)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    
    searcher.setSimilarity(similarities.BM25Similarity())
    #Available similarity: BM25Similarity, MultiSimilarity, PerFieldSimilarityWrapper, SimilarityBase, TFIDFSimilarity
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    if len(sys.argv) < 2:
        run(searcher, analyzer)
    else:
        search_query_from_file(searcher, analyzer, sys.argv[1])
    del searcher
