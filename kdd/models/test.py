import sqlite3
import pandas as pd
import pandas.io.sql as sql
from pandas import Series, DataFrame

df = DataFrame({'A': [1,2,3]})
#df["id"] = df.index

con = sqlite3.connect("test.db")

df.to_sql("test", con)

