#encoding:utf-8
import os

# this script preprocess large files with German and Italian bigrams.
# the process is the same, with exception of the amount of bigrams taken to
# the graph: not 200, but 400.
punct = '”“".,«»\\/*!:;—()\'-%`.?'
tags = ['NOUN', 'VERB', 'ADJ']

def one_link(name):
    d = {}
    total = 0
    graph = open('/home/lyubov_polyanskaya/de_google_graph.ncol', 'a', encoding='utf-8')
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
            if '_' in bi[0] and '_' in bi[1]:
                first = bi[0].split('_')
                second = bi[1].split('_')
                if first[1] in tags and second[1] in tags:
                    if len(first[0]) > 2 and len(second[0]) > 2 and first[0][-1] and second[0][-1] not in punct:
                        bigram = first[0] + ' ' + second[0]
                        if bigram not in d:
                            d[bigram] = freq
                        else:
                            d[bigram] += freq
    if len(d) >= 400:
        for k in sorted(d, key = d.get, reverse = True)[:400]:
            graph.write(k + ' ' + str(round((d[k]/total)*1000000, 2)) + '\n')
    else:
        for k in sorted(d, key = d.get, reverse = True):
            graph.write(k + ' ' + str(round((d[k]/total)*1000000, 2)) + '\n')            
    graph.close()
    os.remove(name) 


links = os.listdir('.')
for link in links:
    if link.startswith('googlebooks'):
        one_link(link)

