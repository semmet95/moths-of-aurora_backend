from selenium import webdriver
import time
from bs4 import BeautifulSoup
import json
import pyrebase

import os

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

username='FB ACCOUNT USER NAME'
password='PASSWORD'

config = {
  "apiKey": "YOUR",
  "authDomain": "CREDENTIALS",
  "databaseURL": "HERE",
  "storageBucket": None
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password('EMAIL ID', 'ASSOCIATED PASSWORD')

createdtime_list=[]
thumbnail_list=[]
link_list=[]
message_list=[]
scraped_data = {}
scraped_data['data']={}

def request_until_succeed(url):
    print("trying the url", url)
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
            print("Retrying.")

    return response.read()

#insert data into the firebase database if new posts found
def check(json_list_1, stored_json):
    somethin_new=False
    for i in range(0, min(len(json_list_1['data']), len(stored_json['data']))):
        if(json_list_1['data'][i]['message'] != stored_json['data'][i]['message']):
            somethin_new=True
            break

    #if(json_list_1['data'][0]['link'] != stored_json['data'][0]['link']):
    #if(json_list_1.items() != stored_json.items()):
    if(somethin_new):
        print('gonna insert')
        db=firebase.database()
        db.child("facebook").set(json_list_1,user['idToken'])
    else:
        print('oops nothing new')

def try_fullsizehref(url, thumbnail_list):
    try:
        driver.get(picparent)
        picparent_soup=BeautifulSoup(driver.page_source, 'html.parser')
        pic_url=picparent_soup.find("div", class_='_57-q').get('data-full-size-href')
        if(pic_url==None):
            return False
        else:
            thumbnail_list.append(pic_url)
            return True
    except:
        return False

#change this to the username of the page you want to scrape
page_name = 'iamAURORA'
#getting profile pic url
picture_url=json.loads(request_until_succeed("https://graph.facebook.com/v2.12/"+page_name+"/picture?type=normal&redirect=false").decode('utf-8'))["data"]["url"]
scraped_data['url']=picture_url

#get to the public page
url="https://m.facebook.com/"
service = webdriver.chrome.service.Service("PATH TO THE CHROMEDRIVER FILE")
service.start()
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options = options.to_capabilities()
driver = webdriver.Remote(service.service_url, options)
driver.get(url)
driver.find_element_by_id('m_login_email').send_keys(username)
time.sleep(2)
driver.find_element_by_id('m_login_password').send_keys(password)
time.sleep(2)
driver.find_element_by_id('u_0_5').click()
time.sleep(5)
driver.find_element_by_xpath("//a[@href='/login/save-device/cancel/?flow=interstitial_nux&nux_source=regular_login']").click()
time.sleep(2)
driver.get('https://m.facebook.com/'+page_name+'/posts/')

# number of times to scroll
scroll_num = 5
#scroll the page to get the required number of posts
for i in range(scroll_num):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)

#starting to scrape, suck it FB
soup_raw=BeautifulSoup(driver.page_source, 'html.parser')
posts=soup_raw.find_all("div", class_="_5rgt _5nk5 _5msi")

#scraping for links to the posts
eles=soup_raw.find_all("a", class_="_5msj")
for ele in eles:
    if ele['href'][0]=='/':
        link_list.append('https://m.facebook.com'+ele['href'])
    else:
        link_list.append('https://m.facebook.com/'+ele['href'])

#visiting each post to get message, created time and thumbnail url
for link in link_list:
    driver.get(link)
    post_soup=BeautifulSoup(driver.page_source, 'html.parser')

    msgdiv=post_soup.find("div", class_='_5rgt _5nk5')
    try:
        message_list.append(msgdiv.text)
    except:
        message_list.append(' ')

    timediv=post_soup.find("div", class_='_52jc _5qc4 _78cz _24u0 _36xo').abbr
    '''time_stamp=''
    for i in range(len(timediv.text)):
        if timediv.text[i].isdigit():
            time_stamp=timediv.text[i:timediv.text.find('·')]
            break'''

    createdtime_list.append(timediv.text)

    try:
        picparent=post_soup.find("div", class_='_5rgu _7dc9 _27x0').find('a')['href']
        if 'https://lm.facebook.com' not in picparent:
            old_method_worked = try_fullsizehref('https://m.facebook.com'+picparent, thumbnail_list)
            if old_method_worked:
                continue
            picparent='https://www.facebook.com'+picparent
            driver.get(picparent)
            picparent_soup=BeautifulSoup(driver.page_source, 'html.parser')
            pic_url=picparent_soup.find("img", class_='scaledImageFitWidth img').get('src')
            if(pic_url==None):
                print("None case for url :", link)
                thumbnail_list.append('NA')
            else:
                thumbnail_list.append(pic_url)
        else:
            print('if not satisfies for url :', link)
            thumbnail_list.append('NA')
    except:
        try:
            driver.find_element_by_xpath('//div[@class="_2zi_ _zgm _2zj0"]').click()
            time.sleep(2)
            post_soup=BeautifulSoup(driver.page_source, 'html.parser')
            vidtag=post_soup.find("div", class_='_53mw').find("video", class_='_2c9v _53mv')
            thumbnail_list.append(vidtag.get('src'))
        except:
            try :
                picparent = link[:8] + 'www' + link[9:]
                driver.get(picparent)
                picparent_soup=BeautifulSoup(driver.page_source, 'html.parser')
                pic_url=picparent_soup.find("img", class_='_3chq').get('src')
                if(pic_url==None):
                    print("double exception None case for url :", link)
                    thumbnail_list.append('NA')
                else:
                    thumbnail_list.append(pic_url)
            except:
                print('triple exception occured for url :', link, 'and picparent :', picparent)
                thumbnail_list.append('NA')

for i in range(len(link_list)):
    temp={'created_time':createdtime_list[i]}
    scraped_data['data'][i]=temp
    scraped_data['data'][i]['full_picture']=thumbnail_list[i]
    scraped_data['data'][i]['link']=link_list[i]
    scraped_data['data'][i]['message']=message_list[i]

#print(scraped_data)
stored_json=json.loads(request_until_succeed("YOUR FIREBASE REALTIME DATABASE URL + .json").decode('utf-8'))
check(scraped_data, stored_json)

driver.close()
driver.quit()
#uncomment this to kill the chrome process after scraping
#os.system('pkill chrome')
