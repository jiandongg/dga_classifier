"""
this script produces the max matching for each domain to it's longest mozilla TLD
since the TLD list is very short, the algorithm is naive and brut force
"""
"""
解析域名的tld（次域名）

need:
1-tld_list.txt,
tld列表
1-conficker_alexa_training.txt
训练集（域名，恶意类别）（恶意（conficker算法生成）为1，不恶意（alexa排名）为0）

output:
1-training_w_tld.txt 训练集（域名，恶意类别，tld）
"""


def max_match(domain, tlds):  # simple match and find the longest match
   match = [i for i in tlds if i in domain] 
   if len(match) > 0:
       for i in sorted(match,key=lambda x: len(x), reverse=True):
           if i == domain[-(len(i)):]:  # longest and matches the end of the domain
               return i
   else: return 'NONE'


tld_file = open('1-tld_list.txt', 'r')
print('tld_file = open(\'1-tld_list.txt\', \'r\')')
tld_list = list('.'+t.strip().strip('.')+'.' for t in tld_file)  # for domain match, add dot as prefix and postfix
tld_file.close()

# fi = open('1393459321.nps_malware_dga_training_set.txt','r')
# fi = open('expanded_training_set.txt','r')
fi = open('1-conficker_alexa_training.txt', 'r')
print('fi = open(\'1-conficker_alexa_training.txt\', \'r\')')

fw = open('11-training_w_tld.txt', 'w')

import tldextract

for f in fi:
    domain, cla = f.strip().split('\t')  # # domain为训练集域名，cla为对应标签（恶意类别）
    # match = max_match(domain, tld_list)
    match = tldextract.extract(domain).suffix
    fw.write('%s\t%s\t%s\n'%(domain,cla,'.'+match+'.'))
print('output:11-training_w_tld.txt, domain, cla, tld')

fw.close()
fi.close()
