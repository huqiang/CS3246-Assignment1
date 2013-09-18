from QueryDocumentParser import QueryDocumentParser

def parse_query_file():

	file = open('CS3246Project1_query.txt')
	contents = unicode(file.read(), 'iso-8859-1')

	query_parser = QueryDocumentParser()
	query_parser.feed(contents)
	return query_parser.contents

'''
Parsed query results:

[{'qid': u'q1', 'query': u'SETL, Very High Level Languages'}, 
{'qid': u'q2', 'query': u'portable operating systems'}, 
{'qid': u'q3', 'query': u'code optimization for space efficiency'}, 
{'qid': u'q4', 'query': u'Optimization of intermediate and machine code'}, 
{'qid': u'q5', 'query': u'Parallel algorithms'}, 
{'qid': u'q6', 'query': u'Graph theoretic algorithms applicable to sparse matrices'}, 
{'qid': u'q7', 'query': u'Applied stochastic processes'}, 
{'qid': u'q8', 'query': u'Performance evaluation and modelling of computer systems'}, 
{'qid': u'q9', 'query': u'Fast algorithm for context-free language recognition or parsing'}, 
{'qid': u'q10', 'query': u'Texture analysis by computer.\tDigitized texture analysis.  Texture synthesis. Perception of texture.'}, 
{'qid': u'q11', 'query': u'The role of information retrieval in knowledge based systems (i.e., expert systems).'}, 
{'qid': u'q12', 'query': u'Dictionary construction and accessing methods for fast retrieval of words or lexical items or morphologically related information. Hashing or indexing methods are usually applied to English spelling or natural language problems.'}, 
{'qid': u'q13', 'query': u'Information retrieval articles by Gerard Salton or others about clustering, bibliographic coupling, use of citations or co-citations, the vector space model, Boolean search methods using inverted files, feedback, etc.  Salton, G.'}, 
{'qid': u'q14', 'query': u'Algorithms for parallel computation, and especially comparisons between parallel and sequential algorithms.'}]
'''
