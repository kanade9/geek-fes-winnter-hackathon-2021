from bs4 import BeautifulSoup
import requests
import subprocess
import spacy
from functools import lru_cache
import numpy as np
import json
import os

nlp = spacy.load('ja_ginza')  

path_csv = os.path.join("..", 'data', 'performers_list.csv')
urls={}
names = {}
with open(path_csv,"r") as fp:
    for i,line in enumerate(fp):
        if i==0:
            continue
        line=line.strip().split(",")
        uid=line[0]
        names[uid] = line[1]
        _urls=line[9:]
        urls[uid]=_urls


def getSentence(url):
    if url=="":
        return ""
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        texts = [s.getText().strip() for s in soup.find_all("p")]
        return texts
    except:
        print("Error",url)
        return [""]


d={}
spacy_doc_dict = {}
for key in urls:
    retval = []
    for l in urls[key]:
        retval+=getSentence(l)#毎回アクセスするの迷惑なので、そのうちキャッシュする。
    d[key]=retval
    spacy_doc_dict[key] = []
    for text in retval:
        try :
            doc = nlp(text)
            spacy_doc_dict[key].append(doc)
        except:
            pass


def getArg(v1,v2):
    return np.dot(v1,v2)/(np.linalg.norm(v1, ord=2)*np.linalg.norm(v2, ord=2))
    
@lru_cache()
def getVectors():
    c = {}
    for key in d:
        c[key]=np.zeros(100,)
        for s in d[key]:
            doc = nlp(s)
            for token in doc:
                c[key] += token.vector
    return c

def search_list(words):
    return search_sentence(" ".join(words))

def get_similarity(uid, userdoc):
    cos_sim = [] 
    for doc in spacy_doc_dict[uid]:
        cos_sim.append(doc.similarity(userdoc))
    if len(cos_sim)>0:
        return max(cos_sim)
    else:
        return -1

def search_sentence(sentence):
    doc_query = nlp(sentence)
    speakers = list(urls.keys())
    speakers = sorted(speakers, key= lambda w: get_similarity(w, doc_query), reverse=True)
    return speakers

def search(x):
    if type(x)==list:
        return search_list(x)
    else:
        return search_sentence(x)

if __name__ == '__main__':
    q = ["ウェブ","人工知能","DX"]
    print(q)
    result= search(q)
    print(result)
    print([names[k] for k in result])



    q = "私は人工知能に興味があります"
    print(q)
    result= search(q)
    print(result)
    print([names[k] for k in result])

    q = "私はRubyに興味があります"
    print(q)
    result= search(q)
    print(result)
    print([names[k] for k in result])