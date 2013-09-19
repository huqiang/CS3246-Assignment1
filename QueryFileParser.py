from QueryDocumentParser import QueryDocumentParser

def parse_query_file(query_file):

	file = open(query_file)
	contents = unicode(file.read(), 'iso-8859-1')

	query_parser = QueryDocumentParser()
	query_parser.feed(contents)
	return query_parser.contents

'''
Parsed query file results:

[{'query_no': u'q1', 'query_content': u'SETL, Very High Level Languages'}, 
{'query_no': u'q2', 'query_content': u'portable operating systems'}, 
{'query_no': u'q3', 'query_content': u'code optimization for space efficiency'}, 
{'query_no': u'q4', 'query_content': u'Optimization of intermediate and machine code'}, 
{'query_no': u'q5', 'query_content': u'Parallel algorithms'}, 
{'query_no': u'q6', 'query_content': u'Graph theoretic algorithms applicable to sparse matrices'}, 
{'query_no': u'q7', 'query_content': u'Applied stochastic processes'}, 
{'query_no': u'q8', 'query_content': u'Performance evaluation and modelling of computer systems'}, 
{'query_no': u'q9', 'query_content': u'Fast algorithm for context-free language recognition or parsing'}, 
{'query_no': u'q10', 'query_content': u'Texture analysis by computer.\tDigitized texture analysis.  Texture synthesis. Perception of texture.'}, 
{'query_no': u'q11', 'query_content': u'The role of information retrieval in knowledge based systems (i.e., expert systems).'}, 
{'query_no': u'q12', 'query_content': u'Dictionary construction and accessing methods for fast retrieval of words or lexical items or morphologically related information. Hashing or indexing methods are usually applied to English spelling or natural language problems.'}, 
{'query_no': u'q13', 'query_content': u'Information retrieval articles by Gerard Salton or others about clustering, bibliographic coupling, use of citations or co-citations, the vector space model, Boolean search methods using inverted files, feedback, etc.  Salton, G.'}, 
{'query_no': u'q14', 'query_content': u'Algorithms for parallel computation, and especially comparisons between parallel and sequential algorithms.'}]
'''
