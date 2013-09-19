class HTMLDocument(object):
	def __init__(self, contents):
		self.contents = contents
		contents_list = contents.split('\n')
		
		open_tag = False
		prop_list, temp_list = [], []
		for i in range(len(contents_list)):
			if len(contents_list[i]) == 0:
				if open_tag:
					open_tag = False
					prop_list.append(temp_list)
					temp_list = []
			else:
				if not open_tag:
					open_tag = True
				temp_list.append(contents_list[i])
		
		def concat_and_strip(item):
			if type(item) == str:
				return item.strip()
			else:
				return ' '.join([i.strip() for i in item]).strip()

		curr_prop_index = 0

		# First prop is document title
		self.title = concat_and_strip(prop_list[curr_prop_index])
		curr_prop_index += 1

		curr_prop = concat_and_strip(prop_list[curr_prop_index])
		
		if curr_prop[0:4] != 'CACM':
			# Document has description
			self.description = curr_prop
			curr_prop_index += 1
			curr_prop = concat_and_strip(prop_list[curr_prop_index])
		else:
			self.description = 'No description available'
		
		date_array = filter(lambda x: len(x) != 0, 
							curr_prop.replace('CACM', ' ').replace(',', ' ').strip().split(' '))
		self.month = date_array[0].strip()
		self.year = date_array[1].strip()

		curr_prop_index += 1

		if '.' in prop_list[curr_prop_index][0]:
			# Document has author(s)
			self.authors = tuple(map(lambda i: i.strip(), prop_list[curr_prop_index]))
			curr_prop_index += 1
		else:
			self.authors = ()

		if prop_list[curr_prop_index][0][0:2] != 'CA':
			self.keywords = tuple(map(lambda i: i.strip().lower(), concat_and_strip(prop_list[curr_prop_index]).split(',')))
			curr_prop_index += 1
		else:
			self.keywords = ()

		while prop_list[curr_prop_index][0][0:2] != 'CA':
			curr_prop_index += 1

		self.timestamp = prop_list[curr_prop_index][0]

		self.contents_array = prop_list

	def has_description(self):
		return self.description == 'No description available'

	def has_authors(self):
		return len(self.authors) > 0

	def has_keywords(self):
		return len(self.keywords) > 0