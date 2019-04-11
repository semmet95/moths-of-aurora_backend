from bs4 import BeautifulSoup
import requests
import json
import datetime
import time

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
	tickets_data=[]
	
	URL = 'https://www.aurora-music.com'
	page = requests.get(URL)
	print("page =", page)    
	html = BeautifulSoup(page.text, "html.parser") # Extract the page's HTML as a string
	
	dates=html.findAll("td", {"class": "umg_live_date"})
	fests=html.findAll("td", {"class": "umg_live_venue"})
	locations=html.findAll("td", {"class": "umg_live_location"})
	url_collection=html.findAll("td", {"class": "umg_live_tickets"})
	urls=[]
	for url_parent in url_collection:
		try:
			url_url=url_parent.find("a", {"class": "umg_live_ticket_link"})['href']
			urls.append(url_url)
		except:
			urls.append("NA")
	
	rsvps=[]
	for rsvp_parent in html.findAll("td", {"class": "umg_live_rsvp"}):
		try:
			rsvp_url=rsvp_parent.find("a", {"class": "umg_live_ticket_link"})['href']
			rsvps.append(rsvp_url)
		except:
			rsvps.append("NA")
		
	tickets_num=len(urls)
	#print("ticket num =", tickets_num, "\nscraped raw data =", html)
	for i in range(tickets_num):
		ticket_object={}
		ticket_object['date']=dates[i].get_text()
		ticket_object['fest']=fests[i].get_text()
		ticket_object['location']=locations[i].get_text()
		ticket_object['url']=urls[i]
		ticket_object['rsvp']=rsvps[i]
		tickets_data.append(ticket_object)
		
	print(tickets_data)
	stored_json=json.loads(request_until_succeed("https://moths-of-aurora.firebaseio.com/tickets.json").decode('utf-8'))
	
	if(str(tickets_data) != str(stored_json) and tickets_num!=0):
		db = firebase.database()
		db.child("tickets").set(tickets_data, user['idToken'])
		print("\n\n\n\nsuccessfully updated database, hope so")
	else:
		print("not updating database and ticket_num =", tickets_num)
	    
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

get_scraped_data()
