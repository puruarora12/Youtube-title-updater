  
#!/usr/bin/python

# Update the snippet metadata for a video. Sample usage:
#   python update_video.py --video_id=<VIDEO_ID> --tags="<TAG1, TAG2>" --title="New title" --description="New description"

import argparse
import os
import sys
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import get_video_info
import time
import googleapiclient.discovery
import datetime


CLIENT_SECRETS_FILE = 'client_secret.json'
time = datetime.time.hour()

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
VIDEO_ID='Rq9rUa_aemA'
# Authorize the request and store authorization credentials.
#def get_authenticated_service():
    #flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    #credentials = flow.run_console()
    #return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def make_title(views,likes,comments):
    TEMPLATE = "This video has %s views and %s likes and %s comments"%(views,likes,comments)
    return TEMPLATE

def update_video(credentials_dict):
    #print("inside update file")
    tags = ["tom scott","youtube title update views","show views in youtube title","youtube data api","v3","api","application program interface"]
    now =datetime.datetime.now().strftime("%H")
    count = 0
    while True:
        if (now >=2 and now <=6):
            x=900
        else:    
            x=180
        
        if (count ==5):
            x*=4
            count=0

        print("loop")
        time.sleep(x) #60 seconds
        info = get_video_info.getinfo()
        updated_title = make_title(info['views'],info['likes'],info['comments'])
        print("1 just before credentials")
        credentials = google.oauth2.credentials.Credentials(credentials_dict["token"],
    refresh_token = credentials_dict["refresh_token"],
    token_uri = credentials_dict["token_uri"],
    client_id = credentials_dict["client_id"],
    client_secret = credentials_dict["client_secret"],
    scopes = credentials_dict["scopes"])


        print("the credentials are ")
        print(credentials)
        print('before youtube line')
        youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
        print('after youtube line')
        
        if(info['title'].strip()==updated_title.strip()):
            count+=1
            continue
        else:
            x=180


        try:
            print('making request')
            request = youtube.videos().update(
				part="snippet",
		        body={
		          "id": VIDEO_ID,
		          "snippet": {
		            "categoryId": 22,
		            "defaultLanguage": "en",
		            "title": updated_title,
		            "description": info['description'],
		            "tags" : tags
		          },

		        })
            print(request)
            print('request written')
            response = request.execute()
            print(response)
            print("request executed")
			#print(response)
            if "error" in response:
				#Some error occured, notify via mail
                try:
                    print("this is the response")
                    print(response)
                except:
                    pass
        except Exception as e:
            try:
                print(e)
            except:
                pass


