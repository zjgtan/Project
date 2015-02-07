#-*- coding: utf-8 -*-

import sys
import dataframe
import math

data_set = "./data/sub_training.txt"

#Click Through Rate
ctr_cols = ["ad", "advertiser", "query", "user"]
if "CTR" in sys.argv:
	for col in ctr_cols:
		exec("""\
click_impr_{0} = dict()""".format(col))

def p_ctr(click_impr_dict, alpha=0.05, beta=75):

	ctr = {}

	for key, (click, impr) in click_impr_dict.items():
		ctr[key] = (click + alpha * beta) / (impr + beta)

	return ctr
	


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


