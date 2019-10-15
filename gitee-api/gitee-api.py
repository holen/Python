#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-03

from flask import Flask, redirect, request
import requests
import json

app = Flask(__name__)
app.debug = True

base_url = "https://gitee.com"
access_token_url = base_url + "/oauth/token"
authorize_url = base_url + "/oauth/authorize"
gitee_api_url = "https://gitee.com/api/v5"

redirect_uri = "http://10.10.10.10:5001/zhl/passport"
client_id = "123"
client_secret = "123"
owner = "abc"
repo = "test"

def getPullRequestsList(access_token, owner, repo, state="open"):
    """ 获取Pull Requests列表 """
    request_url = gitee_api_url + "/repos/{}/{}/pulls".format(owner, repo)
    headers = {
        "Accept": "application/json, text/plain, */*"
    }
    params = {
        "access_token": access_token,
        "owner": owner,
        "repo": repo,
        "state": state
    }
    print(request_url)
    r = requests.get(request_url, headers=headers, data=params)
    print(r.status_code)
    return r.json()

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, world!'

@app.route('/zhl/auth', methods=['GET'])
def client_auth():
    """ 授权认证 """
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "client_secret": client_secret,
        "response_type": "code"
    }
    # r = requests.get(authorize_url, data=params)
    # print(r.url)
    # print(r.status_code)
    uri = authorize_url + "?client_id={}&redirect_uri={}&response_type=code".format(client_id, redirect_uri)
    return redirect(uri)

@app.route('/zhl/passport', methods=['POST', 'GET'])
def client_passport():
    """ 获取码云access_token """
    print(request.args)
    print(request.base_url)
    code = request.args.get('code')
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "client_secret": client_secret
    }
    r = requests.post(access_token_url, data=payload)
    print(r.status_code)
    print(r.json())
    access_token = r.json().get("access_token")
    print(access_token)
    jdata = getPullRequestsList(access_token, owner, repo)
    # print(jdata)
    for data in jdata:
        print(data.get("number"))
    return "access success!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
