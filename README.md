# YT API Parser

## Overview

This repository demonstarates the backend assignment for Fampay in Github Externship.

The server runs a scheduled task that fetches data from youtube using the youtube API.This data is then stored in the servers local database. With help of a GET API you can retrieve the contents of this database in descending order of published datetime of the video. The endpoint for this API is /data

There is provision for adding multiple keys which will be rotated once one key has exhausted its quota.

This application is also deployed on heroku <https://ytapidemo.herokuapp.com/data>

## Deployment

- Clone the Repository
- Create a file named keyfile.py and add your keys as a list of strings in ytkeylist.
- e.g. ``` ytkeylist=['key1','key2'] ```

### Deploying on Heroku

- Create an app on heroku
- Add heroku as a remote to the repository
- Push to heroku master branch

### Deploying on Local Machine

- use pip to install requirements ```pip install -r requirements.txt```
- run gunicorn server to serve the application ```gunicorn app:app```
- goto the url and try getting /data endpoint

## Testing API

The API returns application/json when it recieves a GET request on /data endpoint optional parameter of start.  

### Using curl

```curl -v "https://ytapidemo.herokuapp.com/data"```

this should return code 200 OK

also making start larger than the no of items in db should return a 400 bad request.

You can also check the output returned and modify the size parameter and check the results again for testing.
