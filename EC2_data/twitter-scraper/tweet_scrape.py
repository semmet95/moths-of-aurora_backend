import json
import datetime
import time
import pyrebase

from twython import Twython

config = {
  "apiKey": "YOUR",
  "authDomain": "CREDENTIALS",
  "databaseURL": "HERE",
  "storageBucket": None
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password('EMAIL ID', 'ASSOCIATED PASSWORD')

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

def get_scraped_data():
    tweet_json = scraper()
    #print(tweet_json)
    stored_json=json.loads(request_until_succeed("https://moths-of-aurora.firebaseio.com/twitter.json").decode('utf-8'))
    check(tweet_json, stored_json)
    #db.child("twitter").set(tweet_json, user['idToken'])
    #return json.dumps(scraper())

def check(json_list_1, stored_json):
    #print(json_list_1)
    for a_json in json_list_1:
        a_json['text'] = a_json['full_text']

    if(json_list_1[0]['id_str'] != stored_json[0]['id_str']):
        print('inserting data')
        db=firebase.database()
        db.child("twitter").set(json_list_1,user['idToken'])
		
def request_until_succeed(url):
    req = Request(url)
    success = False
    i=1
    while success is False and i<6:
        i=i+1
        try:
            response = urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print(e)
            time.sleep(30)

            print("Error for URL {}: {}".format(url, datetime.datetime.now()))
            print("Retrying.")

    return response.read()

def scraper():
    APP_KEY = 'TWITTER APP KEY'
    APP_SECRET = 'TWITTER APP SECRET'

    twitter = Twython(APP_KEY, APP_SECRET)

    auth = twitter.get_authentication_tokens()

    OAUTH_TOKEN = auth['oauth_token']
    OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
    twitter = Twython(APP_KEY, APP_SECRET)
    auth = twitter.get_authentication_tokens()
    OAUTH_TOKEN = auth['oauth_token']
    OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
    #print(auth['auth_url'])
    twitter2 = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    user_timeline = twitter.get_user_timeline(screen_name='USER HANDLE TO SRACPE TWEETS OF', tweet_mode='extended')
    return user_timeline

get_scraped_data()
