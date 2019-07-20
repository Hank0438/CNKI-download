import pandas as pd

dfm = pd.read_csv('patent', header=None, names=['company'])
df1 = pd.read_table('referenceDetail1000.txt', sep=' ', header=None, names=['company', 'patentNum'])
df2 = pd.read_table('referenceDetail2000.txt', sep=' ', header=None, names=['company', 'patentNum'])
df3 = pd.read_table('referenceDetail3000.txt', sep=' ', header=None, names=['company', 'patentNum'])
df4 = pd.read_table('referenceDetail4000.txt', sep=' ', header=None, names=['company', 'patentNum'])
df5 = pd.read_table('referenceDetail5000.txt', sep=' ', header=None, names=['company', 'patentNum'])
df6 = pd.read_table('referenceDetail6000.txt', sep=' ', header=None, names=['company', 'patentNum'])
df7 = pd.read_table('referenceDetail7000.txt', sep=' ', header=None, names=['company', 'patentNum'])
df8 = pd.read_table('referenceDetail8000.txt', sep=' ', header=None, names=['company', 'patentNum'])
df9 = pd.read_table('referenceDetail9000.txt', sep=' ', header=None, names=['company', 'patentNum'])
df95 = pd.read_table('referenceDetail9500.txt', sep=' ', header=None, names=['company', 'patentNum'])
df3000 = pd.read_table('totalList.txt', sep=' ', header=None, names=['idx', 'company', 'patentNum'])

dfc = pd.concat([df4, df5, df6, df7, df8, df9, df95, df3000], axis=0, join='inner', ignore_index=True, sort=False)
#dfc = dfcon.append([df4, df5, df6, df7, df8, df9, df95], ignore_index=True, sort=False)
print(len(df1))
print(len(df2))
print(len(df3))
print(len(df4))
print(len(df5))
print(len(df6))
print(len(df7))
print(len(df8))
print(len(df9))
print(len(df95))
#print(dfcon)
#print(dfc)



dfm = pd.merge(dfm, dfc, how='outer', on='company', validate="one_to_one")
#print(dfm)
#print(dfm['patentNum'].isna())
print('NAN: ', dfm['patentNum'].isna().sum())

#dfc3000 = pd.concat([df3000], axis=0, join='inner', ignore_index=True, sort=False)
dfm.to_excel('output.xlsx', 'withNAN')