from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys
import csv


def getRatingValue(item):
    decimal = float(item[-1])
    whole = float(item[-2])
    return(whole + decimal/10)

def find_information(place_url):
    driver.get(place_url)
    
    try:
        title = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div[3]/div/div/div[1]/h1")
        location = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div[3]/div/div/div[3]/span[1]/span/a")
        noOfReviews = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[6]/div/div[1]/div[3]/div/div[1]/div/div[1]/span")
        ratings = driver.find_elements_by_xpath("/html/body/div[2]/div[2]/div[2]/div[6]/div/div[1]/div[3]/div/div[2]/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div/span[2]")

        try:
            food = driver.find_element_by_xpath("//*[@data-tab='TABS_OVERVIEW']/div[@class='ui_columns']/div[1]/div[1]/div[3]/div[2]/div[1]/span[3]/span")
            foodRatingValue = food.get_attribute("class")
            foodRating = getRatingValue(foodRatingValue)
        except:
            foodRating = "None"
        try:
            service = driver.find_element_by_xpath("//*[@data-tab='TABS_OVERVIEW']/div[@class='ui_columns']/div[1]/div[1]/div[3]/div[2]/div[2]/span[3]/span")
            serviceRatingValue = service.get_attribute("class")
            serviceRating = getRatingValue(serviceRatingValue)
        except:
            serviceRating = "None"

        try:
            value = driver.find_element_by_xpath("//*[@data-tab='TABS_OVERVIEW']/div[@class='ui_columns']/div[1]/div[1]/div[3]/div[2]/div[3]/span[3]/span")
            valueRatingValue = value.get_attribute("class")
            valueRating = getRatingValue(valueRatingValue)
        except:
            valueRating = "None"

        try:
            atmosphere = driver.find_element_by_xpath("//*[@data-tab='TABS_OVERVIEW']/div[@class='ui_columns']/div[1]/div[1]/div[3]/div[2]/div[4]/span[3]/span")
            atmosphereRatingValue = atmosphere.get_attribute("class")
            atmosphereRating = getRatingValue(atmosphereRatingValue)
        except:
            atmosphereRating = "None"
    
        try:
            try:
                cuisinePath = driver.find_element_by_xpath("//*[@data-tab='TABS_DETAILS']/div/div/div[2]/div//div[contains(text(),'CUISINE')]/../div[2]")
                cuisine = cuisinePath.text
            except:
                cuisinePath = driver.find_element_by_xpath("//*[@data-tab='TABS_OVERVIEW']/div/div[2]/div/div//div[contains(text(),'CUISINE')]/../div[2]")
                cuisine = cuisinePath.text
        except:
            cuisine = "None"

        try:
            try:
                price = driver.find_element_by_xpath("//*[@data-tab='TABS_DETAILS']/div/div/div[2]/div//div[contains(text(),'PRICE RANGE')]/../div[2]")
                priceRange = price.text
            except:
                price = driver.find_element_by_xpath("//*[@data-tab='TABS_OVERVIEW']/div/div[2]/div/div//div[contains(text(),'PRICE RANGE')]/../div[2]")
                priceRange = price.text
        except:
            priceRange = "None"


        ratingValue = 5
        averageRating = 0
        allReviews = 0

        reviewsNumberTmp = noOfReviews.text
        reviewsNumberTmp = reviewsNumberTmp.replace(',', '')
        reviewsNumberTmp = reviewsNumberTmp[1:]
        reviewsNumberTmp = reviewsNumberTmp[:-1]
        
        for rating in ratings:
            tmp = rating.text
            tmp = tmp.replace(',', '')
            averageRating = averageRating + (ratingValue * int(tmp))
            allReviews = allReviews + int(tmp)
            ratingValue = ratingValue - 1
        averageRating = float(averageRating / allReviews)
        averageRating = round(averageRating, 2)

        return title.text, location.text, int(reviewsNumberTmp), averageRating, cuisine, priceRange, foodRating, serviceRating, valueRating, atmosphereRating
    except:
        print("-----")

PATH = "C:\chromedriver.exe"
driver = webdriver.Chrome(PATH)

currentpage = "https://www.tripadvisor.com/Search?q=slovenia&searchSessionId=0245589C18F1D6164283105A54A805491606936354720ssid&sid=E1083FC871454FBF51FACA5A442B92FF1606936367578&blockRedirect=true&ssrc=e&geo=274862&rf=10"

listOfRestaurants = []
restaurantsInformation = []

for i in range(34):
    print(i)
    driver.get(currentpage + "&o=" + str(i * 30))
    time.sleep(3)
    restaurants = driver.find_elements_by_xpath("//a[@class='review_count']")
    for restaurant in restaurants:
        listOfRestaurants.append(restaurant.get_attribute('href')[:-8])
    for i in range(len(listOfRestaurants)):
        restaurantsInformation.append(find_information(listOfRestaurants[i]))
    listOfRestaurants.clear()

restaurantsInformation = list(filter(None, restaurantsInformation))
print(restaurantsInformation)

filename = "restaurants.csv"
fields = ["Name", "Location", "Number of reviews", "Average rating", "Cuisine", "Price Range", "Food Rating", "Service Rating", "Value Rating", "Atmosphere Rating"]
with open(filename, 'w', encoding="utf-8") as csvfile:  
    csvwriter = csv.writer(csvfile)   
    csvwriter.writerow(fields)   
    csvwriter.writerows(restaurantsInformation)

driver.quit()
