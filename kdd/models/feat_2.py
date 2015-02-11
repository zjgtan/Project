#-*- coding: utf-8 -*-

import pandas as pd
from pandas import Series, DataFrame
import pandas.io.sql as sql
import sqlite3


def compute_ctr(key, table, alpha=0.05, beta=75):
	con = sqlite3.connect("./data/kdd2012.db")
	query = "select click, impr, {0} from {1}".format(key, table)
	df = sql.read_frame(query, con)
	df = df.groupby(key).sum()
	ctr = (df['click'] + alpha * beta) / (df['impr'] + beta)
	ctr = DataFrame({"ctr": ctr})

	try:
		con.execute("""
		CREATE TABLE ctr_{0} (
		id VARCHAR(10) PRIMARY KEY,
		ctr FLOAT
		)
		""".format(key))
	except:
		pass

	query = """insert into ctr_{0} (id, ctr) values (?, ?)""".format(key)
	con.executemany(query, ctr.to_records(index=True))
	con.commit()
	con.close()

'''
compute_ctr("adID", "training_data")
compute_ctr("advertiserID", "training_data")
compute_ctr("queryID", "training_data")
compute_ctr("userID", "training_data")
'''

import math

def compute_tf_idf(table):

	con = sqlite3.connect("./data/kdd2012.db")

	df = sql.read_frame("select * from {0}".format(table), con)

	N_doc = len(df)

	doc_freq = {}
	for (id, text) in df.values:
		words = set(text.rstrip().split("|"))
		for word in words:
			doc_freq.setdefault(word, 0)
			doc_freq[word] += 1

	query = """
	CREATE TABLE tf_idf_{0} (
	id VARCHAR(10),
	word VARCHAR(10),
	weight FLOAT
	)
	""".format(table)

	con.execute(query)
	con.commit()

	for (id, text) in df.values:
		words_count = pd.Series(text.rstrip().split("|")).value_counts().to_dict()
		words_tf_idf = {}
		for word in words_count:
			tf = words_count[word] * 1.0 / sum(words_count.values())
			idf = math.log(N_doc * 1.0/ (doc_freq[word] + 1))

			tf_idf = tf * idf

			query = "INSERT INTO tf_idf_{0} (id, word, weight) values (?, ?, ?)".format(table)

			con.execute(query)
			con.commit()
			con.close()


	
print "load query"
compute_tf_idf("query")
print "load title"
compute_tf_idf("title")
print "load desc"
compute_tf_idf("description")
print "load keyword"
compute_tf_idf("keyword")

	

'''
#TF-IDF
tfidf_cols = ["query", "title", "description", "keyword"]
if "TF-IDF" in sys.argv:
	for col in tfidf_cols:
		exec("""\
{0}_doc_freq = dict()
{0}_id_set = set()
		""".format(col))

CLICK, IMPR, DISPLAYURL, AD, ADVERTISER, DEPTH, POSITION, QUERY, KEYWORD, TITLE, DESCRIPTION, USER = range(12)

for line in file(data_set):
	terms = line.rstrip().split("\t")

	if "CTR" in sys.argv:

		for col in ctr_cols:
			exec("""\
id = terms[{1}] 
click_impr_{0}.setdefault(id, [0, 0]) 
click_impr_{0}[id][0] += int(terms[CLICK])
click_impr_{0}[id][1] += int(terms[IMPR])""".format(col, col.upper()))

	if "TF-IDF" in sys.argv:
		for col in tfidf_cols:
			exec("""\
id = terms[{1}]
{0}_id_set.add(id)""".format(col, col.upper()))

#后处理
if "CTR" in sys.argv:

	for col in ctr_cols:
		exec("""\
ctr_{0} = p_ctr(click_impr_{0})
dataframe.dump_dict("data/ctr_{0}.txt", ctr_{0})""".format(col))
		
title_dict = dataframe.load_dict("../track2/titleid_tokensid.txt")
query_dict = dataframe.load_dict("../track2/queryid_tokensid.txt")
description_dict = dataframe.load_dict("../track2/descriptionid_tokensid.txt")
keyword_dict = dataframe.load_dict("../track2/purchasedkeywordid_tokensid.txt")
user_dict = dataframe.load_dict("../track2/userid_profile.txt", flag=False)


if "TF-IDF" in sys.argv:
	for col in tfidf_cols:
		exec("""\
for id in {0}_id_set:
	words = set({0}_dict[id].rstrip().split("|"))
	for word in words:
		{0}_doc_freq.setdefault(word, 0)
		{0}_doc_freq[word] += 1
		""".format(col))

		exec("""\
fd = open("data/{0}_tf_idf.txt", "w")
num_doc = len({0}_id_set)
for id in {0}_id_set:
	words = {0}_dict[id].rstrip().split("|")
	word_freq = dict()
	for word in words:
		word_freq.setdefault(word, 0)
		word_freq[word] += 1
	word_weight = dict()
	for word in word_freq:
		word_weight[word] = word_freq[word] * 1.0 / max(word_freq.values()) * math.log(num_doc * 1.0 / ({0}_doc_freq[word] + 1))
	word_weight = sorted(word_weight.items(), key=lambda (x, y) : y, reverse=True)
	print >>fd, "\t".join([id] + map(":".join, [(str(x), str(y)) for x, y in word_weight]))
		""".format(col))

'''
