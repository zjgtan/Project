import sqlite3
import sys


def create_table(db_name,  query):
	conn = sqlite3.connect(db_name)
	curs = conn.cursor()

	try:
		curs.execute(query)
	except sqlite3.OperationalError:
		print >> sys.stderr, "table already exits"

	conn.commit()
	conn.close()

def read_file(db_name, file_name, table_name, convert):
	conn = sqlite3.connect(db_name)
	curs = conn.cursor()

	curs.execute("PRAGMA table_info({0})".format(table_name))
	cols = len(curs.fetchall())

	query = 'INSERT INTO {0} VALUES '.format(table_name) + "(" + ", ".join(['?'] * cols) + ")"

	for line in file(file_name):
		fields = line.rstrip().split("\t")
		vals = convert(fields)
		curs.execute(query, vals)
	conn.commit()
	conn.close()

query = """
CREATE TABLE {0} (
id VARCHAR(10),
desc TEXT
)
"""
create_table("./data/kdd2012.db", query.format("description"))
create_table("./data/kdd2012.db", query.format("query"))
create_table("./data/kdd2012.db", query.format("title"))
create_table("./data/kdd2012.db", query.format("keyword"))

query = """
CREATE TABLE {0} (
id VARCHAR(10),
gender INT,
age INT
)
"""
create_table("./data/kdd2012.db", query.format("user"))


print "load description"
read_file("./data/kdd2012.db", "../track2/descriptionid_tokensid.txt", "description", lambda x:  x)
print "load query"
read_file("./data/kdd2012.db", "../track2/queryid_tokensid.txt", "query", lambda x:  x)
print "load title"
read_file("./data/kdd2012.db", "../track2/titleid_tokensid.txt", "title", lambda x:  x)
print "load keyword"
read_file("./data/kdd2012.db", "../track2/purchasedkeywordid_tokensid.txt", "keyword", lambda x:  x)
print "load user"
read_file("./data/kdd2012.db", "../track2/userid_profile.txt", "user", (lambda x:  (x[0], int(x[1]), int(x[2]))))

query = """
CREATE TABLE {0} (
click INT,
impr INT,
displayURL VARCHAR(10),
adID VARCHAR(10),
advertiserID VARCHAR(10),
depth INT,
position INT,
queryID VARCHAR(10),
keywordID VARCHAR(10),
titleID VARCHAR(10),
descriptionID VARCHAR(10),
userID VARCHAR(10)
)
"""

create_table("./data/kdd2012.db", query.format("training_data"))
create_table("./data/kdd2012.db", query.format("validation_data"))

read_file("./data/kdd2012.db", "./data/sub_training.txt", "training_data", lambda x: (int(x[0]), int(x[1]), x[2], x[3], x[4], int(x[5]), int(x[6]), x[7], x[8], x[9], x[10], x[11]))
read_file("./data/kdd2012.db", "./data/validation.txt", "validation_data", lambda x: (int(x[0]), int(x[1]), x[2], x[3], x[4], int(x[5]), int(x[6]), x[7], x[8], x[9], x[10], x[11]))
