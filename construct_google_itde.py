#encoding:utf-8
import re
import gzip
import urllib.request
import os

r = re.compile('<a href="(.+)"(.+)</a>')
punct = '”“".,«»\\/*!:;—()\'-%`.?'
tags = ['NOUN', 'VERB', 'ADJ']

# goes to the bigram archive by the hyperlink, preprocesses the .gz file and adds bigrams to the graph .ncol file
def one_link(l, name):
    d = {}
    total = 0
    graph = open('/home/lyubov_polyanskaya/it_google_graph.ncol', 'a', encoding='utf-8')
    # in case the bigram file is too large (more than 2 GB) and can't be opened by the python function
    # it is written in the 'left.txt' file and than the list of hyperlinks is downloaded by wget on the server
    # and archives are opened with gunzip. The script preprocessing these large file is called 'google_large_itde.py'
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
                if '_' in bi[0] and '_' in bi[1]:
                    first = bi[0].split('_')
                    second = bi[1].split('_')
                    # getting rid of the noise (only bigrams in which the first and the second words have pos NOUN, VERB or ADJ
                    # goes to the graph
                    if first[1] in tags and second[1] in tags:
                        if len(first[0]) > 2 and len(second[0]) > 2 and first[0][-1] and second[0][-1] not in punct:
                            bigram = first[0] + ' ' + second[0]
                            if bigram not in d:
                                d[bigram] = freq
                            else:
                                d[bigram] += freq
        # writing top200 bigrams from the frequency list (or the whole list if there are less than 200 bigrams in the dictionary)
        if len(d) >= 200:
            for k in sorted(d, key = d.get, reverse = True)[:200]:
                graph.write(k + ' ' + str(round((d[k]/total)*1000000, 2)) + '\n') # the ipm value will represent weights in our google graphs
        else:
            for k in sorted(d, key = d.get, reverse = True):
                graph.write(k + ' ' + str(round((d[k]/total)*1000000, 2)) + '\n')            
        graph.close()
        os.remove(name.strip('.gz') + '_') 

    except MemoryError:
        left = open('/home/lyubov_polyanskaya/left.txt', 'a', encoding='utf-8')
        left.write(l)
        left.close()
        try:
            os.remove(name)
        except FileNotFoundError:
            z = 1
        graph.close()

# open the file with hyperlinks to files and start processing
links = open('it_href.txt', 'r', encoding='utf-8')
for link in links:
    href = r.search(link)
    if href is not None:
        hyper = href.group(1)
        f_name = href.group(2)
        one_link(hyper, f_name)
