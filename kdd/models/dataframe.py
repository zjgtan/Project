
def load_line_data_set(filename, s="\t"):

	data = []

	for line in file(filename):
		terms = line.rstrip().split(s)
		data.append(terms)

	return data

def load_dict(filename, s="\t", flag=True):
	d = {}

	for line in file(filename):
		terms = line.rstrip().split(s)
		if flag == True:
			d[terms[0]] = terms[1]
		else:
			d[terms[0]] = line

	return d

def dump_dict(filename, d, s="\t"):

	fd = open(filename, "w")
	for key, value in d.items():
		print >>fd, s.join(map(str, [key, value]))
	fd.close()

