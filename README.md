CS3246-Assignment1
==================

Semester 1 AY13/14

### Members ###
- Hu Qiang 		A0077857
- Tay Yang Shun	A0073063M

### Overview ###
- This program is written in Python 2, and not tested in Python 3.
- This program assumes the IndexFiles.index folder reisides the same directory as the program is.
- The query file is the same format as the given test file.

### How-to-Use ###
1.	Index:
	- $ python IndexFiles.py PATH_TO_DATA_FOLDER
	- e.g. python IndexFiles.py data_project1
2.	Search with query file:
	- $ python SearchFiles.py PATH_TO_QUERY_FILE
	e.g. python SearchFiles.py CS3246Project1_query.txt
3.	Search with user input:
	- $ python SearchFiles.py

### Relevance Feedback ###
- After every round of search, click the checkboxes in the rightmost column for each document to indicate that the respective document is relevant to the search.
- After selecting the relevant documents, click the 'Record Relevance Feedback' button to refine the search with new search terms.
