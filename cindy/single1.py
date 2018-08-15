import porter

# load stopwords into appropriate data structure
stopwords = set()
with open( 'stopwords.txt', 'r' ) as f:
	for line in f:
		stopwords.add(line.rstrip())

# load the porter stemmer
stemmer = porter.PorterStemmer()

# open document collection

f = open( 'npl-doc-text.txt', 'r' )

# 'docs' will be a list of documents
docs = f.read().split('   /')

f.close()

# store term frequencies
all_documents = {}

# iterate through all the docs
for doc in docs:
	# divide this document into its terms
	terms = doc.split()
	if terms[0] != '/': # skip rubbish at the end
		# count terms in this doc
		docdict = {}

		# iterate terms in this doc
		for term in terms[1:]:
			# only do something if it's NOT a stopword
			if term not in stopwords:
				term = stemmer.stem(term)
				# first time I've seen 'term'
				if term not in docdict:
					docdict[term] = 1
				else:
					docdict[term] += 1
		all_documents[terms[0]] = docdict;

# display output
for docid in all_documents:
	# sort terms by frequency
	sorted_terms = sorted( all_documents[docid], key=all_documents[docid].get, reverse=True)

	# most common term more frequent than 1
	if all_documents[docid][sorted_terms[0]] > 1:
		print( '{}:'.format(docid), end='' )
		# print terms with frequency > 1
		i = 0
		while all_documents[docid][sorted_terms[i]] > 1:
			print( ' {} ({})'.format( sorted_terms[i], all_documents[docid][sorted_terms[i]] ), end='' )
			i += 1
		print()
