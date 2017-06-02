#encoding:utf-8
import re
import gzip
import urllib.request
import os
import pymorphy2

r = re.compile('<a href="(.+)".+</a>')

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

# goes to the bigram archive by the hyperlink, preprocesses the .gz file and adds bigrams to the graph .ncol file
def one_link(l, name):
    d = {}
    total = 0
    graph = open('/home/nerdherd16/google_graph.ncol', 'a', encoding='utf-8')
    # in case the bigram file is too large (more than 2 GB) and can't be opened by the python function
    # it is written in the 'left.txt' file and than the list of hyperlinks is downloaded by wget on the server
    # and archives are opened with gunzip. The script preprocessing these large file is called 'google_large_rus.py'
    try:
        response = urllib.request.urlretrieve(l, name)
        with gzip.open(name, 'rt', encoding='utf-8') as f:
            file_content = f.read() 
        outF = open(name.strip('.gz') + '_', 'w', encoding='utf-8')
        outF.write(file_content)
        outF.close()
        os.remove(name)
        print('yea')
        text = open(name.strip('.gz') + '_', 'r', encoding='utf-8')
        print(name)
        for line in text:
            line = line.split('\t')
            bi = line[0]
            year = line[1]
            freq = int(line[3])
            total += freq # the variable which counts the quanitity of bigrams in the file (we need it to count the ipm value)
            if int(year) > 1949: # we take to the graphs bigrams of the texts 1950-2012 
                bi = bi.split()
                # getting rid of the noise
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
        # writing top200 bigrams from the frequency list (or the whole list if there are less than 200 bigrams in the dictionary)
        if len(d) >= 200:
            for k in sorted(d, key = d.get, reverse = True)[:200]:
                graph.write(k + ' ' + str(round((d[k]/total)*1000000, 2)) + '\n') # the ipm value will represent weights in our google graphs
        else:
            for k in sorted(d, key = d.get, reverse = True)[:len(d)]:
                graph.write(k + ' ' + str(round((d[k]/total)*1000000, 2)) + '\n')            
        graph.close()
        os.remove(name.strip('.gz') + '_') 

    except MemoryError:
        left = open('/home/nerdherd16/left.txt', 'a', encoding='utf-8')
        left.write(l)
        left.close()
        try:
            os.remove(name)
        except FileNotFoundError:
            z = 1
        graph.close()

# open the file with hyperlinks to files and start processing
links = open('rus_bigram.txt', 'r', encoding='utf-8')
for link in links:
    href = r.search(link)
    if href is not None:
        hyper = href.group(1)
    f_name = link.split('>')[1].strip('</a>')
    one_link(hyper, f_name)

