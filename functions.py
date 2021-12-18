import sqlite3,requests,json
from datetime import datetime, timedelta, timezone
from keyfile import ytkey

yturl='https://www.googleapis.com/youtube/v3/search'
query='valorant'

time=datetime.now(timezone.utc).astimezone() - timedelta(hours=6)  #get current time and subtract 6 hours from it
mytime = time.isoformat() # get and convert current time to RFC 3339

class key:
    keyworks=True
    def __init__(self,keyid):
        self.keyid=keyid

def ytreq(args): #request youtube for vidinfo
    output=requests.get(yturl, params={'part': 'snippet','q':query,"key": ytkey,'type':'video','order':'date','publishedAfter':mytime})
    output=json.loads(output.content)
    writedb(output)
    print("request made")

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