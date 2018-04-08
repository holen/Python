#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-03
# @Author  : zhl (zhl@qianbitou.cn)

import base64
import random
import time

from flask import Flask, redirect, request
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.debug = True
oauth = OAuth(app)

flask_api_url="http://127.0.0.1:5000"
redirect_uri='{}/client/passport'.format(flask_api_url)
users = {  
    'liuchunming': ['12345']  
}  
client_id = '1234567890'
users[client_id] = []
auth_code = {}
oauth_redirect_uri = []

def gen_token(uid):
    str = b'":".join([str(uid), str(random.random()), str(time.time() + 7200)])'
    token = base64.b64encode(str)
    users[uid].append(token)
    return token

def gen_auth_code(uri):  
    code = random.randint(1,1000)  
    auth_code[code] = uri  
    return code  

def verify_token(token):
    token = b'"{}".format(token)'
    _token = base64.b64decode(token)
    if not users.get(_token.split(':')[0])[-1] == token:
        return -1
    if float(_token.split(':')[-1]) >= time.time():
        return 1
    else:
        return 0

@app.route('/client/login', methods=['POST', 'GET'])
def client_login():
    uri = '{}/oauth?response_type=code&client_id={}&redirect_uri={}'.format(flask_api_url, client_id, redirect_uri)
    return redirect(uri)

@app.route('/oauth', methods=['POST', 'GET'])
def oauth():
    if request.args.get('user'):
        if users.get(request.args.get('user'))[0] == request.args.get('pw') and oauth_redirect_uri:
            uri = oauth_redirect_uri[0] + '?code={}'.format(gen_auth_code(oauth_redirect_uri[0]))
            return redirect(uri)
    if request.args.get('code'):  
        if auth_code.get(int(request.args.get('code'))) == request.args.get('redirect_uri'):  
            return gen_token(request.args.get('client_id'))  
    if request.args.get('redirect_uri'):
        oauth_redirect_uri.append(request.args.get('redirect_uri'))
    return "please login"

@app.route('/client/passport', methods=['POST', 'GET'])
def client_passport():
    code = request.args.get('code')
    uri = '{}/oauth?grant_type=authorization_code&code={}&redirect_uri={}&client_id={}'.format(flask_api_url, code, redirect_uri, client_id)
    return redirect(uri)

@app.route('/testlogin', methods=['POST', 'GET'])
def testlogin():
    token = request.args.get('token')
    return 'Hello' + token

if __name__ == '__main__':
    app.run(debug=True)
