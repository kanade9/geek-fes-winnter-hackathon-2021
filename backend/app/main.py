from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World from Flask"

@app.route("/chokudai", methods=["POST"])
def return_chokudai():
    if request.method == 'POST':
        data = request.data.decode('utf-8')
        data = json.loads(data)
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