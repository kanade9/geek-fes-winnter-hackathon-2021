from flask import Flask, render_template, request, jsonify
import json
import csv
import os
import random


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

@app.route("/")
def hello():
    return "Hello World from Flask"


@app.route("/random", methods=["POST"])
def random_choice():
    if request.method == 'POST':
        data = request.data.decode('utf-8')
        data = json.loads(data)
        keys = random.sample(dict_performers.keys(), 2)
        info = {}
        for i, k in enumerate(keys):
            info[i] = dict_performers[k] 
        print(info)
        return jsonify(info)

@app.route("/chokudai", methods=["POST"])
def return_chokudai():
    if request.method == 'POST':
        data = request.data.decode('utf-8')
        data = json.loads(data)
        print(data)
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