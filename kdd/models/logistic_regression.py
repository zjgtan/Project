from dataframe import *


training_set_file = "data/sub_training.txt"
val_set_file = "data/validation.txt"

description_word_weight = load_dict("data/description_tf_idf.txt")
query_word_weight = load_dict("data/query_tf_idf.txt")
keyword_word_weight = load_dict("data/keyword_tf_idf.txt")
title_word_weight = load_dict("data/title_tf_idf.txt")

ctr_ad = load_dict("data/ctr_ad.txt")
ctr_advertiser = load_dict("data/ctr_advertiser.txt")
ctr_user = load_dict("data/ctr_user.txt")
ctr_query = load_dict("data/ctr_query.txt")


for line in file(:)

