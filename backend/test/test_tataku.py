# coding: utf-8
import json
import requests
import io
import json
import sys

def pytest_generate_tests(metafunc):
    # called once per each test function
    funcarglist = metafunc.cls.params[metafunc.function.__name__]
    argnames = sorted(funcarglist[0])
    metafunc.parametrize(
        argnames, [[funcargs[name] for name in argnames] for funcargs in funcarglist]
    )

class TestFlask:
    params = {
    "test_hello":[
        dict(url="http://0.0.0.0:80")
        ] , 
    "test_chokudai":[
        dict(url="http://0.0.0.0:80")
        ] }

    def test_hello(self, url):
        response = requests.get(url)
        print(response.headers)
        print(response.url)
        print(response.text)
        print(response.headers["content-type"])

    def test_chokudai(self, url):
        url += "/chokudai"
        dic = {"kw": ["フロント", "深層学習"]}
        response = requests.post(url, json.dumps(dic),  headers={'Content-Type': 'application/json'})
        print(response.json())