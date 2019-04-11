from bs4 import BeautifulSoup
import requests
import json

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

def get_scraped_data():
	client_access_token = 'YOUR GENIUS API CLIENT TOKEN'
	#chahge this to the id of the artist you want to scrape the song's lyrics of
	artist_id = 36413
	base_url = 'https://api.genius.com/artists/'+artist_id+'/songs?page='
	page_num=1
	per_page_parameter='&per_page=50'
	url=base_url+str(page_num)+per_page_parameter

	token = 'Bearer {}'.format(client_access_token)
	headers = {'Authorization': token}

	scraped_data = []
	#scraping lyrics of all the songs
	while True :
		response = requests.get(url, headers=headers)
		json_response=json.loads(response.text)
		scraped_data.append(json_response)
		page_num+=1
		
		url=base_url+str(page_num)+per_page_parameter
		
		print("page_num = ", page_num, " and next_page = ", json_response["response"]["next_page"])
		
		if json_response["response"]["next_page"]==None :
			break
		
	scraped_songs=format_scraped_data(scraped_data)
	db = firebase.database()
	db.child("songs").set(scraped_songs, user['idToken'])
	
	#return str(scraped_songs)
	
def format_scraped_data(scraped_data):
	scraped_songs=[]
	for data in scraped_data:
		for songs in data["response"]["songs"]:
			print("scraping lyrics for", songs['title'])
			song_data={}
			song_data['title']=songs['title']
			song_data['song_thumbnail']=songs['song_art_image_thumbnail_url']
			song_data['id']=songs['id']
			song_data['url']=songs['url']
			song_data['lyrics']=get_lyrics_from_url(songs['url'])
			scraped_songs.append(song_data)
	return scraped_songs

def get_lyrics_from_url(URL):
	page = requests.get(URL)    
	html = BeautifulSoup(page.text, "html.parser") # Extract the page's HTML as a string

	# Scrape the song lyrics from the HTML
	lyrics = html.find("div", class_="lyrics").get_text()
	lyrics_text=''.join((c for c in str(lyrics) if ord(c) < 128))
	print(lyrics_text)
	return lyrics_text

get_scraped_data()
