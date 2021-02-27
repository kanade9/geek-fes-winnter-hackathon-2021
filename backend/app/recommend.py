from bs4 import BeautifulSoup
import requests
import MeCab
import subprocess
from gensim.models import Word2Vec
from functools import lru_cache
import numpy as np
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += "HIGH:!DH:!aNULL"#とてもよくない！！！ define hellmanに脆弱性がみつかったのでrequestsが(opensslが?)なんかアップデートされたらしく動かなくなったので、強制的に無視。
cmd = 'echo `mecab-config --dicdir`"/mecab-ipadic-neologd"'
path = (subprocess.Popen(cmd, stdout=subprocess.PIPE,
                           shell=True).communicate()[0]).decode('utf-8')
m = MeCab.Tagger("-d {0} -Owakati".format(path))

urls = {
    "松尾豊":["http://ymatsuo.com/japanese/","https://ja.wikipedia.org/wiki/%E6%9D%BE%E5%B0%BE%E8%B1%8A","https://type.jp/et/feature/13988/"],
    "ちょまど":["https://sakumaga.sakura.ad.jp/entry/2020/09/29/120000?utm_source=chomado&utm_medium=blog&utm_campaign=chomado","https://sakumaga.sakura.ad.jp/entry/2020/08/28/120000?utm_source=chomado&utm_medium=blog&utm_campaign=chomado","https://sakumaga.sakura.ad.jp/entry/2020/07/22/120000?utm_source=chomado&utm_medium=blog&utm_campaign=chomado","https://www.nisc.go.jp/security-site/month/column/200309.html"],
    "田中邦裕":["https://ja.wikipedia.org/wiki/%E7%94%B0%E4%B8%AD%E9%82%A6%E8%A3%95","https://signal.diamond.jp/articles/-/51","https://employment.en-japan.com/myresume/entry/2019/05/22/124716"],
    "小林":["https://fullswing.dena.com/archives/4171","https://dena.com/jp/recruit/career/opf/interview/engineer.html","https://type.jp/et/feature/4457/"],
    "水上":["https://www.accenture.com/jp-ja/blogs/japan-careers-blog/internship02","https://ampmedia.jp/2020/02/28/accenture-technology/","https://techplay.jp/column/217"],
    "田中泰生":["https://www.projectdesign.jp/201912/grow-up-business-designer/007152.php","https://news.mynavi.jp/article/20201211-1580665/"],
    "まつもとゆきひろ":["https://ja.wikipedia.org/wiki/%E3%81%BE%E3%81%A4%E3%82%82%E3%81%A8%E3%82%86%E3%81%8D%E3%81%B2%E3%82%8D","https://employment.en-japan.com/myresume/entry/2019/09/26/103000","https://type.jp/et/feature/11640/"],
    "ちょくだい":["https://ja.wikipedia.org/wiki/%E9%AB%98%E6%A9%8B%E7%9B%B4%E5%A4%A7","https://www.atmarkit.co.jp/ait/articles/0911/17/news102.html","https://dentsu-ho.com/articles/7015"],
    "藤本真樹":["https://type.jp/et/feature/14351/","https://japan.cnet.com/article/35059737/","https://japan.cnet.com/article/35059737/2/","https://labs.gree.jp/blog/2020/12/20974/"],
    "塚本":["https://codezine.jp/article/detail/12041","https://codezine.jp/article/detail/12041?p=2"],
    "西尾":["https://www.cyberagent.co.jp/way/features/list/detail/id=24874"],
}

def getSentence(url):
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
