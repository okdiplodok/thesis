#encoding:utf-8
import sys
import gensim, logging
import networkx
import igraph
import csv

tags = ['A', 'S']

def ncol_write(m, ncolname):
# loading the model
    if m.endswith('.vec'):
        model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
    elif m.endswith('.bin') or m.endswith('.gz'):
        model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
    else:
        model = gensim.models.Word2Vec.load(m)
#making a list of tuples representing our graph. In which tuple there is a word,
#a word which is similar to it and their cosine distance
    arr = []
    for token in model.vocab:
        tag1 = token.split('_')[1]
        if tag1 in tags:
            similar = model.most_similar([token], topn=500)
            for element in similar:
                tag = element[0].split('_')[1]
                if tag in tags:
                    if element[1] >= 0.52: #for Russian, for Italian: 0.65
                        arr.append((token, element[0], str(element[1])))
                    else:
                        break
    with open(ncolname, 'a', encoding='utf-8') as f:
        for e in arr:
            f.write(' '.join(e) + '\n')

#.ncol file is a format where with white space a separated vertices (words in our case)
# and weights (cosine distance)
result = ncol_write('ruscorpora_mean_hs.model.bin', 'rus_word2vec_graph.ncol')

    
