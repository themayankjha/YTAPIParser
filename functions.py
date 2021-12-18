import sqlite3,requests,json
from datetime import datetime, timedelta, timezone
from keyfile import ytkeylist

time=datetime.now(timezone.utc).astimezone() - timedelta(hours=6)  #get current time and subtract 6 hours from it
mytime = time.isoformat() # get and convert current time to RFC 3339

yturl='https://www.googleapis.com/youtube/v3/search'
query='valorant'
ytkeyindex=0


def rotateytkey():
    global ytkeyindex   #allow global access inside function
    if(ytkeyindex==len(ytkeylist)-1):
        ytkeyindex=0
    elif(ytkeyindex<len(ytkeylist)-1):
        ytkeyindex=ytkeyindex+1


def ytreq(): #request youtube for vidinfo
    output=requests.get(yturl, params={'part': 'snippet','q':query,"key": ytkeylist[ytkeyindex],'type':'video','order':'date','publishedAfter':mytime})     #generate a request
    try:    #check if request is 403                     
        int(output.content['error']['code'])==403
        rotateytkey()   #switch keys
        ytreq()     #recall function
    except: #if not 403
        output=json.loads(output.content)   #load content of request output
        writedb(output)     
        print("request made")   #log on server

def searchdb(): #get data from db
    con = sqlite3.connect('static/YTdatabase.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM vidData order by published DESC')
    rows = cur.fetchall()
    con.close()
    return rows

def writedb(output): #write data to db
    con = sqlite3.connect('static/YTdatabase.db')
    cur = con.cursor()
    for vid in output['items']:
        vidid=vid['id']['videoId']
        vidpublish=vid['snippet']['publishedAt']
        vidtitle=vid['snippet']['title']
        viddesc=vid['snippet']['description']
        vidthumbnail=vid['snippet']['thumbnails']['default']['url']
        try:
            cur.execute('INSERT INTO vidData (title, desc, published,thumbnail,vidid)VALUES (?, ?, ?, ?, ?)', (vidtitle,viddesc,vidpublish,vidthumbnail,vidid))
        except:
            pass
    con.commit()
    con.close()