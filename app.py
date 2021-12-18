from flask import Flask, render_template, redirect, url_for, request,json
from flask_apscheduler import APScheduler
from functions import key , makeytrequest, searchdb, writedb
from keyfile import ytkey
import requests

app = Flask(__name__)
yturl='https://www.googleapis.com/youtube/v3/search'
query='valorant'

@app.route('/', methods=['GET'])
def home():
    items =None
    return render_template("dash.html",items=items)

@app.route('/data', methods=['GET'])
def dataout():
    pass

def ytreq(args):
    output=requests.get(yturl, params={'part': 'snippet','q':query,"key": ytkey})
    output=json.loads(output.content)
    writedb(output)

scheduler = APScheduler()
scheduler.add_job(func=ytreq, args=['args'], trigger='interval', id='job', seconds=10)
scheduler.start()

if __name__ == '__main__':
    app.run()