# moths-of-aurora_backend
[Moths of Aurora](https://github.com/singh-95/moths-of-aurora) app's backend hosted on an AWS EC2 instance using Firebase Realtime Database and Cloud Functions.

The backend's purpose is to scrape data from different social media acounts of the artist [Aurora Aksnes](https://aurora-music.com), viz, [Facebook](https://m.facebook.com/iamAURORA/posts/?_rdr), [Instagram](https://www.instagram.com/auroramusic/), [Twitter](https://twitter.com/AURORAmusic) and Youtube and update the [database](https://moths-of-aurora.firebaseio.com/.json) as well as generate notification for the Android app when new activity is detected. It also includes scripts that scrape the artist's [official site](https://aurora-music.com) to get the live shows data, and a script that uses [Genius api](https://docs.genius.com/) to scrape and store lyrics of all the songs released by her that are available on their site.

## Cloud_Function
I have only included the file that you need to modify when implementing Firebase Cloud Functions. The code sets listener on various data nodes and pushes a notification to all the registered devices using the app whenever those data nodes are updated.

## EC2_data
This directory contains all the scrapers, the cronjob file and the requirements file. This content of this directory is stored on the AWS EC2 instance I'm using.
All the scrapers download data from their corresponding sites and update a shared firebase realtime database if the downloaded data is not the same as the already stored data.

### fb-scraper
I couldn't create a Facebook App because my requests kept getting denied. So I had to use selenium and scrape the mobile version of the Facebook site to get all the data. Thanks to [this](https://hackernoon.com/is-it-still-possible-to-scrape-facebook-data-yes-it-is-fb4255ba792b) article for the idea.
The script gets the url of the account's profile picture using FB's graph api. Then it uses a chromedriver file (included in the repository, for linux) to first login to facebook then visit the FB page and scrape all the posts by visiting them one by one. You can uncomment `options.add_argument('--headless')` to perform this operation in the background. The script scrapes each post's:
- time of creation
- thumbnail url
- link
- message

### insta-scraper
This script scrapes instagram posts from the artist's instagram page. I used the code from [this](https://github.com/rarcega/instagram-scraper) repo and modified it a bit for my own use.

### twitter-scraper
This script uses the [Twython](https://github.com/ryanmcgrath/twython) library to scrape tweets. I had to create twitter developer account and then create an app to get the required credentials. You can check out the instructions following the link.

### youtube-scraper
Now this script uses a Heroku app to scrape youtube for videos related to the artist. I took the code from [this](https://github.com/HermanFassett/youtube-scrape) repo and changed the url to
`var url = 'https://www.youtube.com/results?search_query=aurora+aksnes+-"mobile+legends"+-"camille"&search_sort=video_date_uploaded';` (check out the `sheltered-tundra-55930` folder)
to get the search results using the relevant keywords. Now, this js script is hosted on Heroku and it returns search results based on the number of pages to scrape provied in the GET request.
In the script `scraped-data-formatter.py`, I'm getting ssearch results from 5 pages. The following details of the vidoes are stored in the database:
- duration
- title
- upload date
- uploader
- video url
- number of views

### lyrics-scraper
This script is used to scrape all the songs and their lyrics stored in the [Genius](https://genius.com/) database using their [api](https://docs.genius.com/). I had to find the artist id for Aurora Aksnes first though.
The scripts doesn't check for new content before inserting the scraped data into the database because no cloud function is set for it's corresponding data node.

### ticket-scraper
Last one, phew. This one scrapes Aurora's [official site](https://aurora-music.com) for data on her live shows which incude:
- date
- fest at which the live is to be held
- location
- ticket links

### crontab
The scripts have to be run regularly to keep the database updated. This is where cron jobs come in. It runs all the above scrapes at regular interval with frequency depending on the corresponding activity. For instance, the twitter scraper is run more frequently than the lyrics scraper because new tweets are made more frequently than new songs.

### requirements.txt
All the packages you need to install to run the code.
