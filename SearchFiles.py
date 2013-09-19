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
from HTMLDocumentParser import HTMLDocumentParser
import QueryFileParser
import RelevanceFileParser
from MyAnalyzer import MyAnalyzer

def perform_user_query(searcher, analyzer):
    while True:
        print
        print "Hit enter with no input to quit."
        command = raw_input("Query: ")
        if command == '':
            return

        print
        print "Searching for: ", command
        query = QueryParser(Version.LUCENE_CURRENT, "contents", analyzer).parse(command)
        hits = searcher.search(query, 50).scoreDocs
        print "%s total matching documents." % len(hits)

        rank = 1
        for hit in hits:
            doc = searcher.doc(hit.doc)
            detailed_format = False
            if detailed_format:
                print 'Rank: ', rank
                print 'Path: ' + doc.get("path") + doc.get("filename")
                print 'Score: ', hit.score
                print 'Title: ', doc.get("title")
                print 'Synopsis: ', doc.get("description")[:200] + '...' , '\n'
            else:
                print rank, doc.get("filename"), doc.get("title")
            rank += 1

def results_comparison(searcher, analyzer, query_file):
    query_data = QueryFileParser.parse_query_file(query_file)
    relevance_data = RelevanceFileParser.parse_relevance_file()
    for query in query_data:
        qid = query['query_no']
        relevant_docs = relevance_data[qid]
        query = QueryParser(Version.LUCENE_CURRENT, "contents", analyzer).parse(query['query_content'])
        hits = searcher.search(query, 50).scoreDocs
        accurate_hits = 0
        for hit in hits:
            doc = searcher.doc(hit.doc)
            if doc.get("filename")[:4] in relevant_docs:
                accurate_hits += 1
        print "Recall" 
        print qid + ': ' + str(accurate_hits) + '/' + str(len(relevant_docs))
        print "Precision" 
        print qid + ': ' + str(accurate_hits) + '/' + str(len(hits))

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
    # analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    analyzer = MyAnalyzer(Version.LUCENE_CURRENT)
    if len(sys.argv) < 2:
        perform_user_query(searcher, analyzer)
    else:
        # search_query_from_file(searcher, analyzer, sys.argv[1])
    # perform_user_query(searcher, analyzer)
        results_comparison(searcher, analyzer, sys.argv[1])
    del searcher
