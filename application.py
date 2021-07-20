import os
import flask
import requests
import time
import argparse

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import update
import threading

import get_video_info
import json
import ast
import smtplib
import multiprocessing

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

application = app = flask.Flask(__name__)
print('started from app ')

app.secret_key = 'randomkey'






Started =False

@app.route('/')
def hello():
    return "hello"
    #gotdata= get_video_info.getinfo()
    #print(gotdata)
    #update.update_video()

@app.route('/test')

def test_api_request():
  global Started 
  
  if Started:
        return "Already Started"
  if 'credentials' not in flask.session:
    return flask.redirect('authorize')
  
  # Load credentials from the session.
  credentials = google.oauth2.credentials.Credentials(
      **flask.session['credentials'])
  
  drive = googleapiclient.discovery.build(
      API_SERVICE_NAME, API_VERSION, credentials=credentials)

  #files = drive.files().list().execute()
 

  # Save credentials back to session in case access token was refreshed.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  flask.session['credentials'] = credentials_to_dict(credentials)
  

  
  t1 = threading.Thread(target=update.update_video , args=[flask.session['credentials']])
  #t2.daemon=True
  #t1.daemon=True
  t1.start() 
  
  #Started =True
  #print('returning after update file')
  return "The code is working in Background"
  
  

def rtpage():
      print("thread 2 started")

      return "done"

@app.route('/testing')
def fin():
     
      return "done page"
        


@app.route('/authorize')
def authorize():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)
   
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
   
    authorization_url, state = flow.authorization_url(
      # Enable offline access so that you can refresh an access token without
      # re-prompting the user for permission. Recommended for web server apps.
      access_type='offline',
      # Enable incremental authorization. Recommended as a best practice.
      include_granted_scopes='true')
    
  # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state
    
    print(authorization_url)
    return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():

  # Specify the state when creating the flow in the callback so that it can
  # verified in the authorization server response.
    
    state = flask.session['state']
    
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
    
  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)
    
  # Store credentials in the session.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)
    
    #return "return from oauth "
    return flask.redirect(flask.url_for('test_api_request'))




def credentials_to_dict(credentials):
      return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


if __name__=='__main__':
    print('started from main')
    app.run(  debug=True)