from flask import Flask, render_template, make_response, request ,jsonify
from flask_apscheduler import APScheduler
from functions import ytreq, searchdb

app = Flask(__name__)


@app.route('/data', methods=['GET'])    #set api endpoint
def dataout():
    try:    #check if start is an integer
        start=int(request.args.get("start",1))
        out=searchdb()
        if(start>len(out)):     #check if start exceeds length
            raise Exception("")
        elif(start+5<len(out)):     #check if last page
            next='/data?start='+str(start+5)
        else:
            next='None'     #set next to none on last page
        results=[]
        try:    #check for list outofbound 
            for num in range(start-1,start+4):      #separate and paginate data
                items=out[num]
                dbid=items[0]
                vidid=items[5]
                vidpublish=items[3]
                vidtitle=items[1]
                viddesc=items[2]
                vidthumbnail=items[4]
                infodict={'dbid':dbid,'vidid':vidid,'vidtitle':vidtitle,'viddesc':viddesc,'vidpublish':vidpublish,'vidthumbnail':vidthumbnail}
                results.append(infodict)
        except: #stop and do nothing if out of bounds
            pass
        return make_response(jsonify(count=len(out),next=next,results=results), 200)    #return data with OK
    except:
        return make_response(jsonify(error="Please Check syntax."),400)     #return error with bad request



scheduler = APScheduler()
scheduler.add_job(func=ytreq, trigger='interval', id='job', seconds=100)
scheduler.start()

if __name__ == '__main__':
    app.run()