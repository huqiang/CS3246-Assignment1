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
import re

class FileSearcher(object):

    def __init__(self, searcher, analyzer):
        self.searcher = searcher
        self.analyzer = analyzer
        self.current_query_str = ""

    def perform_user_query(self, searcher, analyzer):
        root = Tk()
    
        def search():
            search_terms = e.get()
            if len(search_terms.strip()) > 0:
                hits = self.perform_search(search_terms)

                self.update_table(tb, hits)
    
                
            else:
                tb.reset_table()
    
        def clear():
            v.set('')
    
        def record_relevant_results():
            relevant_docs_ids = tb.get_checked_results() # do something with returned list of relevant docs
            new_query = self.form_new_query_from_rf(relevant_docs_ids)
            hits = self.perform_search(self.current_query_str + " " + new_query)
            self.update_table(tb, hits)
    
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
        
        rf = Button(root, text="Record Relevance Feedback", width=30, command=record_relevant_results)
        rf.pack()
    
        root.mainloop()
    
    def form_new_query_from_rf(self, relevant_doc_ids):
        firstSet  = True
        new_query = set()
        for id in relevant_doc_ids:
            doc          = self.searcher.doc(id)
            contents     = re.sub('[/\*&^%$#@?\'`":()<>]', " ", doc.get("title")).strip()
            query        = QueryParser(Version.LUCENE_CURRENT, "contents", self.analyzer).parse(contents)
            keywords     = query.toString().split("contents:")
            keywords_set = set()
            for k in keywords:
                if k.strip() != "":
                    keywords_set.add(k)
            if firstSet:
                new_query = set(keywords_set)
            else:
                new_query = new_query & set(keywords_set)
                firstSet  = False
        return " ".join(new_query)
    
    def perform_search(self, query_str):
        query_str = re.sub('[/\*&^%$#@:"()<>?\'`]', " ", query_str).strip()
        self.current_query_str = query_str
        # print "Searching for: ", query_str
        query = QueryParser(Version.LUCENE_CURRENT, "title", analyzer).parse(query_str)
        title_hits = searcher.search(query, 50).scoreDocs
        title_set = set([hit.doc for hit in title_hits])
        if len(title_hits) > 0:
            max_title_score = max([hit.score for hit in title_hits])

        query = QueryParser(Version.LUCENE_CURRENT, "contents", analyzer).parse(query_str)
        content_hits = searcher.search(query, 50).scoreDocs         
        content_set = set([hit.doc for hit in content_hits])
        if len(content_hits) > 0:
            max_content_score = max([hit.score for hit in content_hits])

        hits = title_set & content_set

        def calculate_new_score(hit):
            score_doc = {'doc': hit}
            title_doc = filter(lambda x: x.doc == hit, title_hits)
            content_doc = filter(lambda x: x.doc == hit, content_hits)
            new_score = 0.5 * (title_doc[0].score/max_title_score) + 0.5 * (content_doc[0].score/max_content_score)
            score_doc['score'] = new_score
            return score_doc

        new_hits_with_scores = [calculate_new_score(hit) for hit in hits]
        new_hits_with_scores.sort(key=lambda x: x['score'], reverse=True)
        sorted_hits = [x['doc'] for x in new_hits_with_scores]
        # print "%s total matching documents." % len(sorted_hits)
        return sorted_hits[:15]

    def update_table(self, tb, hits):
        rank = 1
        results_list = []
        for hit in hits:
            print hit
            doc = searcher.doc(hit)
            results_list.append([rank, doc.get('filename'), doc.get('title'), doc.get("description")[:200], None])
            detailed_format = True
            if detailed_format:
                print 'Rank: ', rank
                print 'File: ', doc.get("filename")
                print 'Title: ', doc.get("title")
                print 'Synopsis: ', doc.get("description")[:200] + '...' , '\n'
            else:
                print rank, doc.get("filename"), doc.get("title")
            rank += 1
        tb.reset_table()
        tb.results_lucene_id_list = hits
        for i in range(len(results_list)):
            for j in range(len(results_list[i])):
                tb.set(j, i+1, results_list[i][j])
    

    def results_comparison(self, searcher, analyzer, query_file):
        query_data = QueryFileParser.parse_query_file(query_file)
        relevance_data = RelevanceFileParser.parse_relevance_file()

        total_FB = 0
        total_recall = 0
        total_precision = 0

        for q in query_data:
            qid = q['query_no']
            relevant_docs = relevance_data[qid]

            hits = self.perform_search(q['query_content'])

            # print hits

            accurate_hits = 0
            for hit in hits:
                doc = searcher.doc(hit)
                if doc.get("filename") in relevant_docs:
                    accurate_hits += 1
            
            recall = float(accurate_hits)/len(relevant_docs)
            if len(hits) == 0:
                precision = 0
            else:
                precision = float(accurate_hits)/len(hits)
            if precision + recall != 0:
                FB = 2 * precision * recall / (precision + recall)
            else:
                FB = 0.0
            
            total_recall += recall
            total_precision += precision
            total_FB += FB

            print '%3s Recall: %.6f  Precision: %.6f  FB: %.6f' % (qid, recall, precision, FB)

        query_data_length = len(query_data)
        avg_recall = total_recall/query_data_length
        avg_precision = total_precision/query_data_length
        avg_FB = total_FB/query_data_length

        print 'Avg Recall: %.6f  Avg Precision: %.6f Avg FB: %.6f' % (avg_recall, avg_precision, avg_FB)

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
    fs = FileSearcher(searcher, analyzer)
    if len(sys.argv) < 2:
        fs.perform_user_query(searcher, analyzer)
    else:
        fs.results_comparison(searcher, analyzer, sys.argv[1])
    del searcher
