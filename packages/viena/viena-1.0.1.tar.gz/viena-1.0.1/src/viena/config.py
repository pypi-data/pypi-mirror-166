import logging
import os
import sqlite3
import threading
from flask import Flask, request
import urllib
from flask import Flask
from flask.json import jsonify
from flask_cors import CORS, cross_origin
import glob
import time
from flask import json
from pathlib import Path

app = Flask(__name__)
CORS(app, support_credentials=True)

list1 = []
nsfw_data=[]

@app.route('/postdata', methods=['POST', 'GET'])
@cross_origin(origin="*")
def createvideo():
    # print("content_type")
    content_type = request.headers.get('Content-Type')
    # print("content_type")
    # print(content_type)
    if (content_type == 'application/json'):
        filelist = request.json
    print(filelist)
    list1.append(filelist)
    # print(list1)
    return "success"


@app.route('/getdata')
@cross_origin(origin="*")
def getdata():
    data = append()
    response = app.response_class(
        response=json.dumps(data,indent=4, sort_keys=False),
        status=200,
        mimetype='application/json'
    )
    return response



@app.route('/getnsfwvideos')
@cross_origin(origin="*")
def getnsfwvideos():
    #send all videos that have nsfw true
    #send videoids and path
    return


@app.route('/getnsfwvideodetails')
@cross_origin(origin="*")
def getnsfwvideodetails():
    #get video, and nsfw frame details
    return

@app.route('/getframe')
@cross_origin(origin="*")
def getframe():
    #using sdk get the frame from the server and send
    return

def append():
    data =list1
    return data


host_name = "0.0.0.0"
port = 5000

if __name__ == '__main__':
    app.run(host=host_name, port=5000, debug=True, use_reloader=False)
    # threading.Thread(target=lambda: app.run(host=host_name, port=port, debug=True, use_reloader=False)).start()
    logging.info("App started")