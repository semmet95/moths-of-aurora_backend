import json
import time
import datetime
from bs4 import BeautifulSoup
import requests

import pyrebase
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
    json_list = getScrapedYoutubeData()
    stored_json=json.loads(request_until_succeed("https://moths-of-aurora.firebaseio.com/youtube.json").decode('utf-8'))
    check(json_list, stored_json)

def check(json_list_1, stored_json):
    if(json_list_1[0]['url'] != stored_json[0]['url']):
        db=firebase.database()
        db.child("youtube").set(json_list_1,user['idToken'])
        print('lol inserting')

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

def getScrapedYoutubeData():
    #I'm using a third party heroku app that scrapes youtube to get the latest videos
    base = 'https://sheltered-tundra-55930.herokuapp.com/?page='
    scraped_data = []

    for i in range(1, 6):
        url = base + str(i)
        responses = requests.get(url)
        data_str = responses.text
        soup = BeautifulSoup(data_str, 'lxml')
        p_string = str(soup.find_all('p'))
        p_string = p_string[4:len(p_string)-5]
		
        print("response_json =", p_string)
        videos = json.loads(p_string)
        for json_obj in videos['results']:
            json_video = json_obj['video']
            video_data = {}
            video_data['title'] = json_video['title']
            video_data['url'] = json_video['url']
            video_data['duration'] = json_video['duration']
            video_data['upload_date'] = json_video['upload_date']
            video_data['views'] = json_video['views']
            video_data['uploader'] = json_obj['uploader']['username']
            scraped_data.append(video_data)
    return scraped_data

get_scraped_data()
