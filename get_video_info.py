#Get's video's likes, dislikes, views, and comments.

import os
import requests
import json
import urllib.parse
import datetime

#VIDEO_ID = "fs_l_rovfBk" #Test video Teja Swaroop Channel
VIDEO_ID = "Rq9rUa_aemA"
API_KEY = "AIzaSyANDZkMbXzCWNZgorvM15D3DjScuFCd5CY"
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def getinfo():
        resp = {}
        url = "https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet&id=%s&key=%s"%(VIDEO_ID,API_KEY)
        #urllib.parse.urlencode(url)

        headers = {
        "Accept" : 'application/json'
        }
        r = requests.get(url,headers=headers)
        j = json.loads(r.text)
        #print(j)
        stats = j['items'][0]['statistics']
        title = j['items'][0]['snippet']['title']
        desc = j['items'][0]['snippet']['description']
        resp['title'] = title
        resp['description'] = desc
        resp['views'] = stats['viewCount']
        resp['likes'] = stats['likeCount']
        resp['dislikes'] = stats['dislikeCount']
        resp['comments'] = stats['commentCount']
        #print(resp)
        return resp

if __name__=="__main__":
	getinfo()

#getinfo()


