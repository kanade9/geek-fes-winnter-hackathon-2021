from bs4 import BeautifulSoup
import requests
import MeCab
import subprocess
from gensim.models import Word2Vec
from functools import lru_cache
import numpy as np
import json
import os
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += "HIGH:!DH:!aNULL"#とてもよくない！！！ define hellmanに脆弱性がみつかったのでrequestsが(opensslが?)なんかアップデートされたらしく動かなくなったので、強制的に無視。
cmd = 'echo `mecab-config --dicdir`"/mecab-ipadic-neologd"'
path = (subprocess.Popen(cmd, stdout=subprocess.PIPE,
                           shell=True).communicate()[0]).decode('utf-8')
m = MeCab.Tagger("-d {0} -Owakati".format(path))

path_csv = os.path.join("..", 'data', 'performers_list.csv')
urls={}
with open(path_csv,"r") as fp:
    for line in fp:
        line=line.strip().split(",")
        uid=line[0]
        _urls=line[9:]
        urls[uid]=_urls


def getSentence(url):
    if url="":
        return ""
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.content)
    texts = [s.getText().strip() for s in soup.find_all("p")]
    return texts


d={}
for key in urls:
    retval = []
    for l in urls[key]:
        retval+=getSentence(l)#毎回アクセスするの迷惑なので、そのうちキャッシュする。
    d[key]=retval

model = Word2Vec.load("/w2v/wiki.model")
def getArg(v1,v2):
    return np.dot(v1,v2)/(np.linalg.norm(v1, ord=2)*np.linalg.norm(v2, ord=2))
@lru_cache()
def getVectors():
    c = {}
    for key in d:
        c[key]=np.zeros(200,)
        for s in d[key]:
            words = m.parse(s).strip().split(" ")
            for word in words:
                try:
                    c[key] += model.wv[word.lower()]
                except KeyError:
                    print(word)
    return c

def search(words):
    v_query = np.zeros(200,)
    for word in words:
        v_query+=model.wv[word.lower()]
    speakers = list(urls.keys())
    sorted(speakers, key= lambda w: getArg(getVectors()[w], v_query))
    return speakers

if __name__ == '__main__':
    print(search(["ウェブ","人工知能","DX"]))
