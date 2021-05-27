from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys
import csv

def find_information(place_url):
    driver.get(place_url)
    try:
        title = driver.find_element_by_xpath("//*[@id='HEADING']")
        location = driver.find_element_by_xpath("//*[@id='NEARBY_TAB']/div[2]/div[1]/div[2]/div[2]/div[1]/span[2]")
        noOfReviews = driver.find_element_by_xpath("//*[@id='REVIEWS']/div/span[1]/span[2]/span[1]")
        ratings = driver.find_elements_by_xpath("/html/body/div[2]/div[2]/div[2]/div[10]/div/div[2]/div/div/div[3]/div/div[1]/div[1]/div[1]/ul/li/span[2]")
        popularReviewMentions = driver.find_elements_by_xpath("/html/body/div[2]/div[2]/div[2]/div[10]/div/div[2]/div/div/div[3]/div/div[1]/div[3]/div[2]/div[3]/button")
        ratingValue = 5
        averageRating = 0

        reviewsNumberTmp = noOfReviews.text
        reviewsNumberTmp = reviewsNumberTmp.replace(',', '')
        
        for rating in ratings:
            tmp = rating.text
            tmp = tmp.replace(',', '')
            averageRating = averageRating + (ratingValue * int(tmp))
            ratingValue = ratingValue - 1
        averageRating = float(averageRating / int(reviewsNumberTmp))
        averageRating = round(averageRating, 2)

        keywords = []
        for item in popularReviewMentions:
            keywords.append(item.text)
        del(keywords[:1])
        while("" in keywords) : 
            keywords.remove("")

        return title.text, location.text, int(reviewsNumberTmp), averageRating, keywords
    except:
        print("-----")

PATH = "C:\chromedriver.exe"
driver = webdriver.Chrome(PATH)

currentpage = "https://www.tripadvisor.com/Search?q=slovenia&searchSessionId=0245589C18F1D6164283105A54A805491606936354720ssid&sid=E1083FC871454FBF51FACA5A442B92FF1606936367578&blockRedirect=true&ssrc=A&geo=274862&rf=6"

listOfPlaces = []
placesInformation = []

for i in range(34):
    driver.get(currentpage + "&o=" + str(i * 30))
    time.sleep(3)
    places = driver.find_elements_by_xpath("//a[@class='review_count']")
    for place in places:
        listOfPlaces.append(place.get_attribute('href')[:-8])
    for i in range(len(listOfPlaces)):
        placesInformation.append(find_information(listOfPlaces[i]))
    listOfPlaces.clear()

placesInformation = list(filter(None, placesInformation))
print(placesInformation)

filename = "things_to_do.csv"
fields = ["Name", "Location", "Number of reviews", "Average rating", "Keywords"]
with open(filename, 'w', encoding="utf-8") as csvfile:  
    csvwriter = csv.writer(csvfile)   
    csvwriter.writerow(fields)   
    csvwriter.writerows(placesInformation)

driver.quit()