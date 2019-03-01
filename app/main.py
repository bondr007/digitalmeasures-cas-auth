
import flask
from flask import Flask,redirect,request
from flask_cas import CAS
from flask_cas import login_required

import hashlib
import hmac
import base64

import urllib.parse
from datetime import datetime
import datetime
import secrets
import os

app = Flask(__name__)
cas = CAS(app, '/cas')
app.config['CAS_SERVER'] = os.environ['CAS_URL']
app.config['CAS_AFTER_LOGIN'] = 'route_root'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.secret_key = secrets.token_bytes() # generate secret from signing cookies

#Test info:
#DMS_PROD_baseURL = "https://www.digitalmeasures.com/login/dm/faculty/authentication/HMACTest.do"
#DMS_PROD_key = "1234567890123456"
DMS_PROD_baseURL = os.environ['DMS_URL']
DMS_PROD_key = os.environ['DMS_KEY']
DMS_PROD_KeyValInSeconds = 66

@app.route('/')
@app.route('/dms')
@login_required
def route_root():
    now = datetime.datetime.utcnow()
    now = now + datetime.timedelta(seconds=DMS_PROD_KeyValInSeconds)  

    now_iso8601 = now.replace(microsecond=0).isoformat() + 'Z'
    queryString = urllib.parse.urlencode({'username': cas.username, 'validUntil': now_iso8601})
    sig = make_digest(queryString)
    queryString = urllib.parse.urlencode({'username': cas.username, 'validUntil': now_iso8601,'signature': sig })
    print(queryString)
    return redirect(DMS_PROD_baseURL + "?" + queryString, code=302)


def make_digest(message):
    #https://github.com/danharper/hmac-examples#python-3
    message = bytes(message, 'utf-8')
    secret = bytes(DMS_PROD_key, 'utf-8')
    hash = hmac.new(secret, message, hashlib.sha1)
    # to lowercase hexits
    hexed = hash.hexdigest()
    #print(hexed)
    # to base64
    based64ed = base64.b64encode(hash.digest())
    #print(based64ed)
    return based64ed


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)