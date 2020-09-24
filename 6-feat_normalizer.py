'''
this script reads in the feature table before vectorizing, and normalize all numerical features from 0 to 1
'''
import pandas as pd
import numpy as np
black_list = ['ip', 'class', 'tld']

'''
input:
5-features.txt 训练集向量

output:
6-features_norm.txt 训练集归一化向量
'''

print('input:\n\
5-features.txt 训练集向量\n\
\n\
output:\n\
6-features_norm.txt 训练集归一化向量')

feat_table = pd.read_csv('5-features.txt', delimiter='\t')

header = list(feat_table.columns)
feat_matrix = pd.DataFrame()
for i in header:
    if i in black_list:
        feat_matrix[i]=feat_table.loc[:,i]
    else:
        line = feat_table.loc[:,i]
        mean_ = line.mean()
        max_ = line.max()
        min_ = line.min()
        feat_matrix[i]=(line-mean_)/(max_-min_)
    print('converted %s'%i)

feat_matrix.to_csv('6-features_norm.txt')
