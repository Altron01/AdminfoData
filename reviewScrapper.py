import csv
from bs4 import BeautifulSoup
import requests

file = open("DataCleaner/reviews.csv", "w")
file.write("id~decision~helpfulReview~funnyReview~hoursPlayed~postDate~reviewText~userCountry\n")

url = ('http://steamcommunity.com/app/%s'
       '/homecontent/?userreviewsoffset=%d'
       '0&p=%d'
       '&workshopitemspage=%d'
       '&readytouseitemspage=%d'
       '&mtxitemspage=%d'
       '&itemspage=%d'
       '&screenshotspage=%d'
       '&videospage=%d'
       '&artpage=%d'
       '&allguidepage=%d'
       '&webguidepage=%d'
       '&integratedguidepage=%d'
       '&discussionspage=%d'
       '&numperpage=10&browsefilter=toprated&browsefilter=toprated&appid=612880&appHubSubSection=10&appHubSubSection=10&l=english&filterLanguage=default&searchText=&forceanon=1'
       )

with open('DataCleaner/gameData.csv', newline='') as myFile:
    reader = csv.reader(myFile, delimiter='~')
    next(myFile)
    for row in reader:
        id = row[0]
        code = row[1].split("/")[4]
        for i in range(1, 3):
            page_url = url % (code, i - 1, i, i, i, i, i, i, i, i, i, i, i, i)
            page_req = requests.get(page_url)
            page_data = BeautifulSoup(page_req.text).find_all("div", {"class": "apphub_Card modalContentLink interactable"})

            for review in page_data:

                help_data = review.find("div", {"class": "found_helpful"}).get_text().split("helpful")
                try:
                    helpful_review = help_data[0]
                    funny_review = help_data[1]
                except:
                    helpful_review = funny_review = ""

                try:
                    recommended = review.find("div", {"class": "title"}).get_text()
                except:
                    recommended = ""
                try:
                    hours_played = review.find("div", {"class": "hours"}).get_text()
                except:
                    hours_played = ""

                precise_data = review.find("div", {"class": "apphub_CardTextContent"}).get_text().split("\t")
                try:
                    post_date = precise_data[0]
                except:
                    post_date = ""

                try:
                    review_text = precise_data[precise_data.__len__() - 4]
                except:
                    review_text = ""

                user_url = review.find("div", {"class": "apphub_friend_block_container"}).find("a").get("href")
                user_request = requests.get(user_url)
                user_profile = BeautifulSoup(user_request.text)

                try:
                    user_country = user_profile.find("div", {"class": "header_real_name ellipsis"}).get_text().split(", ")[2]
                except:
                    user_country = ""

                recommended = ("".join(recommended.split("\n")))
                helpful_review = ("".join(helpful_review.split("\n")))
                funny_review = ("".join(funny_review.split("\n")))
                hours_played = ("".join(hours_played.split("\n")))
                post_date = ("".join(post_date.split("\n")))[:-1]
                review_text = ("".join(review_text.split("\n")))
                user_country = ("".join(user_country.split("\n")))

                recommended = ("".join(recommended.split("\r")))
                helpful_review = ("".join(helpful_review.split("\r")))
                funny_review = ("".join(funny_review.split("\r")))
                hours_played = ("".join(hours_played.split("\r")))
                post_date = ("".join(post_date.split("\r")))
                review_text = ("".join(review_text.split("\r")))
                user_country = ("".join(user_country.split("\r")))

                print(id)

                file.write(id + "~" + recommended + "~" + helpful_review + "~" + funny_review + "~" + hours_played + "~" + post_date + "~" + review_text + "~" + user_country + "\n")

myFile.close()
file.close()