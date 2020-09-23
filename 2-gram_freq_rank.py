from collections import defaultdict
import tldextract  # TLD division, don't care about private tld, default
"""
this script generate the reference rank list of unigram, bigram, trigram from alexa top 100k
"""
"""
生成bigram/trigram的基准排名

need:
2-private_tld.txt 私有域名列表
2-top-100k.csv alexa前10w的域名及其排名

output:
2-n_gram_rank_freq.txt 正例域名的（gram类型, gram组合, 频次, 排名）
"""


def bigrams(words):
    wprev = None
    for w in words:
        if not wprev==None:
            yield (wprev, w)
        wprev = w


def trigrams(words):
    wprev1 = None
    wprev2 = None
    for w in words:
        if not (wprev1 == None or wprev2 == None):
            yield (wprev1,wprev2, w)
        wprev1 = wprev2
        wprev2 = w


private_tld_file = open('2-private_tld.txt', 'r')
print('private_tld_file = open(\'2-private_tld.txt\', \'r\')')
private_tld = set(f.strip() for f in private_tld_file)  # black list for private tld
private_tld_file.close()

unigram_rank = defaultdict(int)
bigram_rank = defaultdict(int)
trigram_rank = defaultdict(int)

fi = open('2-top-100k.csv', 'r')
print('fi = open(\'2-top-100k.csv\', \'r\')')
for f in fi:
    rank, domain = f.strip().split(',')
    ext = tldextract.extract(domain)
    tld = ext.suffix
    main_domain = '$'+ext.domain+'$'  # add begin and end
    if tld in private_tld:
        tld_list = tld.split('.')
        tld = tld_list[-1]
        main_domain = '$'+tld_list[-2]+'$'
    for i in main_domain[1:-1]:
        unigram_rank[i] += 1
    for i in bigrams(main_domain):
        bigram_rank[''.join(i)] += 1
    for i in trigrams(main_domain):
        trigram_rank[''.join(i)] += 1

fi.close()

fw = open('2-n_gram_rank_freq.txt', 'w')
print('output:2-n_gram_rank_freq.txt 1/2/3 items freq rank')
for rank,(i,freq)in enumerate(sorted(unigram_rank.items(), key = lambda x:x[1], reverse = True)):
    try:
        fw.write('1,%s,%d,%d\n'%(i,freq,rank+1))
    except UnicodeEncodeError:
        continue
for rank,(i,freq) in enumerate(sorted(bigram_rank.items(),key = lambda x:x[1], reverse = True)):
    try:
        fw.write('2,%s,%d,%d\n'%(i,freq,rank+1))
    except UnicodeEncodeError:
        continue
for rank,(i,freq) in enumerate(sorted(trigram_rank.items(),key = lambda x:x[1], reverse = True)):
    try:
        fw.write('3,%s,%d,%d\n'%(i,freq,rank+1))
    except UnicodeEncodeError:
        continue

fw.close()
