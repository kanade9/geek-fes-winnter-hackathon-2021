from flask import Flask, render_template, request, jsonify
import json
import csv
import os
import random
import datetime



def read_ccv_to_dict(path: str):
    dic_performers = {}
    with open(path, "r") as f : 
        d = csv.DictReader(f)
        for row in d:
            #rowはdictionary
            #row["column_name"] or row.get("column_name")で必要な項目を取得することができる
            # print(row)
            dic_performers[row["UID"]] = {k:row[k] for k in row.keys() if k != "UID"}
    return dic_performers

app = Flask(__name__)
path_csv = os.path.join("..", 'data', 'performers_list.csv')
dict_performers = read_ccv_to_dict(path_csv)
n_performers = len(dict_performers)

def recommedate_random(kws: list):
    print(dict_performers.keys())
    uids = random.sample(dict_performers.keys(), 4)
    return uids

def date_str_to_date_time(date, start_time):
    connected_str = date + " " + start_time
    dt = datetime.datetime.strptime(connected_str, '%Y/%m/%d %H:%M')
    return dt

def filer_by_date(recommend_infos : dict):
    # 貪欲に時間が重なっているものを削除する
    filtered  = []
    time_set = set()
    dt_now = datetime.datetime.now() 
    for info in recommend_infos:
        dt = date_str_to_date_time(info['date'], info['start_time'])
        if not dt in time_set and dt >= dt_now:
            filtered.append(info)
            time_set.add(dt)
    return filtered 

@app.route("/")
def hello():
    return "Hello World from Flask"


@app.route("/recommend", methods=["POST"])
def recommend():
    if request.method == 'POST':
        data = request.data.decode('utf-8')
        data = json.loads(data)
        uids = recommedate_random(data['kw'])


@app.route("/random", methods=["POST"])
def random_choice():
    if request.method == 'POST':
        data = request.data.decode('utf-8')
        if len(data)>0:
            data = json.loads(data)
        else:
            data = {"kw":[]}
        uids = recommedate_random(data['kw'])
        info = {}
        recommend = [] 
        for i, k in enumerate(uids):
            recommend.append( dict_performers[k] )
        recommend = filer_by_date(recommend) # 貪欲に時間が重なっているものを削除する
        info = { i:info for  i , info in enumerate( recommend) }  
        print(info)
        return jsonify(info)

@app.route("/chokudai", methods=["POST"])
def return_chokudai():
    if request.method == 'POST':
        data = request.data.decode('utf-8')
        if len(data)>0:
            data = json.loads(data)
        else:
            data = {"kw":[]}
        info_chokudai = {
                "name":"高橋 直大", 
                "postion":"AtCoder株式会社 代表取締役社長",
                "start_time":"15:50", 
                "end_time":"16:50",
                "title":"RedCoderのライブ競プロ～競プロ世界ランカーのアルゴリズム改善～", 
                "twitter":"https://twitter.com/chomado" ,
            }
        chokudai_dict = { i:info_chokudai for i in range(3) }
        return jsonify(chokudai_dict)



if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)