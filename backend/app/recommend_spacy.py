from bs4 import BeautifulSoup
import requests
import subprocess
import spacy
from functools import lru_cache
import numpy as np
import json
import os
from collections import defaultdict

nlp = spacy.load('ja_ginza')  

path_csv = os.path.join("..", 'data', 'performers_list.csv')
urls={}
names = {}
titles = {}
positons={}
n_all_text = 0
n_of_text_token_isin = defaultdict(lambda : 1 )

def idf(token: str):
    return np.log( max(n_all_text, 0) / n_of_text_token_isin[token]) 


with open(path_csv,"r") as fp:
    for i,line in enumerate(fp):
        if i==0:
            continue
        line=line.strip().split(",")
        uid=line[0]
        names[uid] = line[1]
        titles[uid] = line[7]
        positons[uid] = line[2]
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
    spacy_doc_dict[key] = {"article":[], 'title':nlp(titles[key]), 
        'name': nlp(names[key]), 'position':nlp(positons[key]),
         'tf':[],
         }
    for text in retval:
        try :
            n_all_text +=1
            doc = nlp(text)
            # idf tabeleupdate
            spacy_doc_dict[key]['article'].append(doc)
            token_list = [str(t) for t in doc]
            tf = defaultdict(lambda :0)
            for t in token_list:
                tf[t] += 1 / (len(token_list) + 1)
            spacy_doc_dict[key]['tf'].append(tf)
            token_set = set(token_list)
            for t in token_set:
                n_of_text_token_isin[t] +=1 
        except:
            pass

def userdoc_tf_idf_vec(userdoc):
    vec = np.zeros(300,)
    tf = defaultdict(lambda :0)
    for t in userdoc:
        tf[str(t)] += 1 / (len(userdoc)+1)
    for t in userdoc:
        vec += t.vector * tf[str(t)] * idf(str(t))
    return vec

def getArg(v1,v2):
    return np.dot(v1,v2)/(np.linalg.norm(v1, ord=2)*np.linalg.norm(v2, ord=2))
    
@lru_cache()
def getVectors():
    c = {}
    for key in d:
        c[key]=np.zeros(300,)
        for s in d[key]:
            doc = nlp(s)
            for token in doc:
                c[key] += token.vector
    return c

def search_list(words):
    return search_sentence(" ".join(words))

def get_similarity(uid, userdoc):
    cos_sim = [] 
    similarity = 0
    vec_user =userdoc_tf_idf_vec(userdoc) 
    for doc, tf in zip(spacy_doc_dict[uid]['article'], spacy_doc_dict[uid]['tf']):
        vec_text = np.zeros(300)
        for t in doc:
            vec_text += t.vector * tf[str(t)] * idf(str(t))
        cos_sim.append(getArg(vec_text, vec_user))
    if len(cos_sim)>0:
        similarity =  np.max(cos_sim)
    else:
        similarity = -1
    similarity += max( getArg(userdoc_tf_idf_vec(spacy_doc_dict[uid]['title']), vec_user), 0 )

    similarity += count_named_entity(uid, userdoc)
    similarity += count_unvector_common_words(uid, userdoc) 
    return similarity 

def count_common_words(uid, userdoc):
    total_count = 0
    counter = {}
    for token in userdoc:
        counter[str(token)] = 0
        for doc in spacy_doc_dict[uid]['article']:
            for t in doc:
                if str(t) == str(token) :
                    counter[str(token)] += 1
        total_count += counter[str(token)]
    if len(counter) > 0:
        return total_count / len(counter)
    else:
        return 0

def count_unvector_common_words(uid, userdoc):
    total_count = 0
    counter = {}
    for token in userdoc:
        if not token.has_vector:
            counter[str(token)] = 0
            for doc in spacy_doc_dict[uid]['article']:
                for t in  doc:
                    if str(t) == str(token) :
                        counter[str(token)] += 1
            for tag in ['name', 'title', 'position']:
                for t in  spacy_doc_dict[uid][tag]:
                    if str(t) == str(token) :
                        counter[str(token)] += 1
            total_count += counter[str(token)]
    if len(counter) > 0:
        return total_count / len(counter)
    else:
        return 0

def count_named_entity(uid, userdoc):
    total_count = 0
    counter = {}
    for token in userdoc.ents:
        counter[str(token)] = 0
        for doc in spacy_doc_dict[uid]['article']:
            for t in  doc.ents:
                if str(t) == str(token) :
                    counter[str(token)] += 1
        for tag in ['name', 'title', 'position']:
            for t in  spacy_doc_dict[uid][tag].ents:
                if str(t) == str(token) :
                    counter[str(token)] += 1
        total_count += counter[str(token)]

    return total_count

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

    q = "Ruby"
    print(q)
    result= search(q)
    print(result)
    print([names[k] for k in result])


    q = "東京大学"  
    print(q)
    result= search(q)
    print(result)
    print([names[k] for k in result])