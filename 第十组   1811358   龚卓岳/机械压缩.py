import pandas as pd

comments=pd.read_csv('comments.csv',encoding='utf-8',header=None)
comments=comments.set_index(0,drop=True)
