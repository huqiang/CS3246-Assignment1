#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"
MAX_NUMBER_OF_SEARCH_RESULTS = 15

import sys, os, lucene
from Tkinter import *
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
from ResultsTable import *

def perform_user_query(searcher, analyzer):
    root = Tk()

    def search():
        search_terms = e.get()
        if len(search_terms.strip()) > 0:
            print "Searching for: ", search_terms
            query = QueryParser(Version.LUCENE_CURRENT, "contents", analyzer).parse(search_terms)
            hits = searcher.search(query, MAX_NUMBER_OF_SEARCH_RESULTS).scoreDocs
            print "%s total matching documents." % len(hits)

            rank = 1
            results_list = []
            for hit in hits:
                doc = searcher.doc(hit.doc)

                results_list.append([rank, doc.get('filename'), doc.get('title'), doc.get("description")[:200], None])

                detailed_format = True
                if detailed_format:
                    print 'Rank: ', rank
                    print 'File: ', doc.get("filename")
                    print 'Score: ', hit.score
                    print 'Title: ', doc.get("title")
                    print 'Synopsis: ', doc.get("description")[:200] + '...' , '\n'
                else:
                    print rank, doc.get("filename"), doc.get("title")
                rank += 1
            tb.reset_table()
            for i in range(len(results_list)):
                for j in range(len(results_list[i])):
                    tb.set(j, i+1, results_list[i][j])
        else:
            tb.reset_table()

    def clear():
        v.set('')

    def record_relevant_results():
        tb.get_checked_results()

    w = Label(root, text="Enter your search terms in the box below")
    w.pack()

    v = StringVar()
    e = Entry(root, takefocus=True, textvariable=v)
    e.bind("<Return>", lambda x: search())
    e.pack()

    b = Button(root, text="Search", width=10, command=search)
    b.pack()

    c = Button(root, text="Clear", width=10, command=clear)
    c.pack()

    tb = ResultsTable(root, MAX_NUMBER_OF_SEARCH_RESULTS + 1, 5)
    tb.pack(side="top", fill="x")
    tb.reset_table()
    
    rf = Button(root, text="Record Relevant Results", width=10, command=record_relevant_results)
    rf.pack()

    root.mainloop()

def results_comparison(searcher, analyzer, query_file):
    query_data = QueryFileParser.parse_query_file(query_file)
    relevance_data = RelevanceFileParser.parse_relevance_file()
    for query in query_data:
        qid = query['query_no']
        relevant_docs = relevance_data[qid]
        query = QueryParser(Version.LUCENE_CURRENT, "keyword", analyzer).parse(query['query_content'])
        hits = searcher.search(query, 50).scoreDocs
        accurate_hits = 0
        for hit in hits:
            doc = searcher.doc(hit.doc)
            if doc.get("filename").replace('html', '') in relevant_docs:
                accurate_hits += 1
        print qid
        print 'Recall: ' + str(round(float(accurate_hits)/len(relevant_docs), 6))
        if len(hits) != 0:
            print 'Precision: ' + str(round(float(accurate_hits)/len(hits), 6))
        else:
            print 'Precision: 0.0'
        print

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
        results_comparison(searcher, analyzer, sys.argv[1])
    del searcher
