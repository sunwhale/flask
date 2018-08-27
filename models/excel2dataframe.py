# -*- coding: utf-8 -*-

import pandas as pd

df = pd.read_excel("info.xlsx")

data = df.to_dict(orient='records')

for d in data:
	print d[u'编号']