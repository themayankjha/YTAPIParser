from flask import Flask, render_template, redirect, url_for, request
from flask_apscheduler import APScheduler
from functions import key , ytreq

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    items =None
    return render_template("dash.html",items=items)

@app.route('/data', methods=['GET'])
def dataout():
    pass

scheduler = APScheduler()
scheduler.add_job(func=ytreq, args=['args'], trigger='interval', id='job', seconds=100)
scheduler.start()

if __name__ == '__main__':
    app.run()