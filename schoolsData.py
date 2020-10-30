import urllib.request
import json
from datetime import datetime
import tweepy
import config
import random
import os.path
from os import path

auth = tweepy.OAuthHandler(config.consumerKey, config.consumerSecret) #authentication keys required to login and tweet from the account
auth.set_access_token(config.accessToken, config.accessTokenSecret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True) #wrapping the Twitter API

try:
    api.verify_credentials() #verifying the credentials
    print("Authentication OK")
except:
    print("Error during Authentication")

url = 'https://data.ontario.ca/api/3/action/datastore_search?resource_id=7fbdbb48-d074-45d9-93cb-f7de58950418' #url to retrieve the cases data
fileobj = urllib.request.urlopen(url) #opens URL
data = json.loads(fileobj.read()) #loads the data in json format
today = datetime.today().strftime('%d/%m/%Y') #sets the current date

currentMax = data['result']['total'] #sets the total number of records
currentData = data['result']['records'] #gets the current data

for record in currentData: #for loop to retrieve the current data for the day
    if record['_id'] == 35: #currently set to a hard number as the data API by the government was released today with some issues
        currentStudents = record['cumulative_school_related_student_cases']
        currentStaff = record['cumulative_school_related_staff_cases']
        currentUnspec = record['cumulative_school_related_unspecified_cases']
        currentSchools = record['current_schools_w_cases']
        newStudents = record['new_school_related_student_cases']
        newStaff = record['new_school_related_staff_cases']
        newUnspec = record['new_school_related_unspecified_cases']
        newSchools = record['new_total_school_related_cases']
        totalCases = record['cumulative_school_related_cases']
        schoolsClosed = record['current_schools_closed']

#creating and formatting of tweet
tweet = ("Ontario School Covid Cases for " + str(today) + "\n\nNew -\nStudent cases: " + str(newStudents) + "\n" + "Staff cases: " + str(newStaff) + "\n" + "Unspecified: " + str(newUnspec) + "\n\n" + 
"Current -\nStudent cases: " + str(currentStudents) + "\n" + "Staff cases: " + str(currentStaff) + "\n" + "Unspecified: " + str(currentUnspec) +  "\n" +
"Total cases: " + str(totalCases) + "\n" + "Schools w/ cases: " + str(currentSchools) + "\n" + "Schools closed: " + str(schoolsClosed) + "\n\n"
"@Sflecce\n@fordnation\n@ONeducation\n@ONThealth\n#COVID19")

#prints out the length of the tweet and the tweet itself
print(len(tweet))
print(tweet)

#the following is the code to allow for pictures to be attached to the tweets
#a text file is created to record which image was used last as files in the images folder are named a number from 1-5
#the script retrieves the last used image from the file and uses a random number generator to retrieve the next image making sure to never use the same image twice in a row
if path.exists("imgName.txt") == False:
    f = open("imgName.txt", "w")

fRead = open("imgName.txt", "r")
lastImgName = fRead.readline()
lastImgNameInt = int(lastImgName)

imgNum = random.randint(1, 5)
while imgNum == lastImgNameInt:
    imgNum = random.randint(1,5)

print(imgNum)

#writes the image name used into the file
f = open("imgName.txt", "w")
f.write(str(imgNum))
f.close

#retrieves the next image to be used from the folder
imgFile = ".\images\\" + str(imgNum) + ".jpg"
print(imgFile)

#publishes the tweet with the image
#api.update_status(tweet, )
api.update_with_media(imgFile, tweet)