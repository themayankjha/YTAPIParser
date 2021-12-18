from flask import Flask, render_template, redirect, url_for, request,json
from flask_apscheduler import APScheduler

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    pass

@app.route('/data', methods=['GET'])
def dataout():
    pass

def ytreq(args):
    pass

if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.add_job(func=ytreq, args=['args'], trigger='interval', id='job', seconds=10)
    scheduler.start()
    app.run()