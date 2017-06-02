#encoding:utf-8

import os
import pymorphy2

# this script preprocess large files with Russian bigrams.
# the process is the same, with exception of the amount of bigrams taken to
# the graph: not 200, but 400.

stop_words_a = [',', '.', '!', ')', '«', '*', '"', ':', '-', '--', ';',
                '...', '?', '»', '(', 'п', 'на', 'у', 'не', 'да',
                'и', 'с', 'по', 'ни', 'или', 'же', 'из', 'во',
                'быть', 'нас', 'в', 'от', 'будет', '..', 'за', 'к',
                'для', 'до', 'н', '\'', '/', 'ли', 'до', 'был', 'как',
                '1', 'бы', 'со', 'нет', 'о', 'буду', 'идет', 'мой',
                'ь', 'уже', 'даже']

stopwords = open('stoplist.txt', 'r', encoding='utf-8').readlines()

tags = ['ADJS', 'COMP', 'NUMR', 'ADVB', 'NPRO', 'PRED', 'PREP', 'CONJ', 'PRCL', 'INTJ']

morph = pymorphy2.MorphAnalyzer()


def one_link(name):
    d = {}
    total = 0
    graph = open('/home/nerdherd16/google_graph.ncol', 'a', encoding='utf-8')
    print('yea')
    text = open(name, 'r', encoding='utf-8')
    print(name)
    for line in text:
        line = line.split('\t')
        bi = line[0]
        year = line[1]
        freq = int(line[3])
        total += freq
        if int(year) > 1949:
            bi = bi.split()
            if bi[0][0] not in 'ЙЦУКЕНГШЩЗХХХЪФЫВАПРОЛДЖЭЁЯЧСМИТЬБЮ' and bi[1][0] not in 'ЙЦУКЕНГШЩЗХХХЪФЫВАПРОЛДЖЭЁЯЧСМИТЬБЮ' and bi[0][0] not in stop_words_a and bi[1][0] not in stop_words_a and bi[0][0] not in 'qwertyuiopasdfghjklzxcvbnmQWERTYUIIIOPASDFGHJKLZXCVBNM' and bi[1][0] not in 'qwertyuiopasdfghjklzxcvbnmQWERTYUIIIOPASDFGHJKLZXCVBNM' and bi[0] not in stopwords and bi[1] not in stopwords:
                first = morph.parse(bi[0].split('_')[0])[0]
                second = morph.parse(bi[1].split('_')[0])[0]
                if 'LATN' not in first.tag and 'LATN' not in second.tag and 'PNCT' not in first.tag and 'PNCT' not in second.tag and 'NUMB' not in first.tag and 'NUMB' not in second.tag and 'intg' not in first.tag and 'intg' not in second.tag and 'real' not in first.tag and 'real' not in second.tag and 'UNKN' not in first.tag and 'UNKN' not in second.tag and 'ROMN' not in first.tag and 'ROMN' not in second.tag:
                    if first.tag.POS not in tags and second.tag.POS not in tags:
                        bigram = first.normal_form + ' ' + second.normal_form
                        if bigram not in d:
                            d[bigram] = freq
                        else:
                            d[bigram] += freq
    if len(d) >= 400:
        for k in sorted(d, key = d.get, reverse = True)[:400]:
            graph.write(k + ' ' + str(round((d[k]/total)*1000000, 2)) + '\n')
    else:
        for k in sorted(d, key = d.get, reverse = True)[:len(d)]:
            graph.write(k + ' ' + str(round((d[k]/total)*1000000, 2)) + '\n')            
    graph.close()
    os.remove(name) 


links = os.listdir('.')
for link in links:
    if link.startswith('googlebooks'):
        one_link(link)
