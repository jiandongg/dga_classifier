import math
from collections import Counter
import tldextract  # TLD
# from publicsuffix import PublicSuffixList
'''
input:

2-private_tld.txt   私有域名列表

1-training_w_tld.txt    训练集（域名，class，tld）

2-n_gram_rank_freq.txt  正例域名的（gram类型, gram组合, 频次, 排名）

output:

3-gram_ranks_training.txt   训练集的(domain,class,gram1排名,gram2排名,gram3排名,主域名)

'''


def ave(list_):  # 计算队列平均值
    if len(list_) == 0:
        return 0
    else:
        return sum(list_)/float(len(list_))


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
        if not (wprev1==None or wprev2==None):
            yield (wprev1, wprev2, w)
        wprev1 = wprev2
        wprev2 = w


private_tld_file = open('2-private_tld.txt', 'r')
print('private_tld_file = open(\'2-private_tld.txt\', \'r\')')
private_tld = set(f.strip() for f in private_tld_file)  # black list for private tld
private_tld_file.close()

fi = open('1-training_w_tld.txt', 'r')
print('fi = open(\'1-training_w_tld.txt\', \'r\')')
fw = open('3-gram_ranks_training.txt', 'w')
print('output:3-gram_ranks_training.txt')
fw.write('domain,class,s1,s2,s3,core\n')
print('n_gram_file = open(\'2-n_gram_rank_freq.txt\', \'r\')')
n_gram_file = open('2-n_gram_rank_freq.txt', 'r')
gram_rank_dict = dict()
for i in n_gram_file:
    cat, gram, freq, rank = i.strip().split(',')
    gram_rank_dict[gram] = int(rank)
n_gram_file.close()

for f in fi:
    domain, cla, tld = f.strip().split('\t')
    strip_domain = domain
    # if not tld=='NONE':
    #    strip_domain = domain[:-len(tld)]
    # strip_domain=strip_domain.strip('.')
    # main_domain = '$'+strip_domain.split('.')[-1]+'$'
    ext = tldextract.extract(strip_domain)  # user tld extractor for more precision
    if len(ext.domain)>4 and ext.domain[:4]=='xn--':  # remove non-ascii domain
        continue
    main_domain = '$'+ext.domain+'$'  # add begin and end
    tld = ext.suffix
    # check if it is a private tld
    if tld in private_tld:
        tld_list = tld.split('.')  # quick hack: if private tld, use its last part of top TLD
        tld = tld_list[-1]
        main_domain = '$'+tld_list[-2]+'$'  # and overwrite the main domain
    unigram_rank = [gram_rank_dict[i] if i in gram_rank_dict else 0 for i in main_domain[1:-1]]  # 一次扫描主域名，计算其排名队列
    bigram_rank = [gram_rank_dict[''.join(i)] if ''.join(i) in gram_rank_dict else 0 for i in bigrams(main_domain)]#extract the bigram
    trigram_rank = [gram_rank_dict[''.join(i)] if ''.join(i) in gram_rank_dict else 0 for i in trigrams(main_domain)]#extract the bigram

    try:
        fw.write('%s,%s,%.2f,%.2f,%.2f,%s\n'%(domain,cla,ave(unigram_rank),ave(bigram_rank),ave(trigram_rank),main_domain))
    except UnicodeEncodeError:
        # some unicode problem for some strange domains
        continue

fw.close()
fi.close()
