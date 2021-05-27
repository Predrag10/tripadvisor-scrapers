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

def find_information(hotel_url):
    driver.get(hotel_url)
    time.sleep(1)

    try:
        title = driver.find_element_by_id("HEADING")
        titleText = title.text
        location = driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div[6]/div/div/div/div[2]/div/div[2]/div/div[1]/div/span[2]/span")
        locationText = location.text
        noOfReviews = driver.find_element_by_xpath("//*[@id='REVIEWS']/div/span[1]/span[2]/span[1]/span[1]")
        ratings = driver.find_elements_by_xpath("/html/body/div[2]/div[2]/div[2]/div[7]/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div[1]/ul/li/span[2]")
        ratingValue = 5
        averageRating = 0
        description = ""
        amenities = []
        reviewsNumberTmp = noOfReviews.text
        reviewsNumberTmp = reviewsNumberTmp.replace(',', '')
    
        for rating in ratings:
            tmp = rating.text
            tmp = tmp.replace(',', '')
            averageRating = averageRating + (ratingValue * int(tmp))
            ratingValue = ratingValue - 1
        if (int(reviewsNumberTmp) != 0):
            averageRating = float(averageRating / int(reviewsNumberTmp))
            averageRating = round(averageRating, 2)

        try:
            hotelClassValue = driver.find_element_by_xpath("//*[@id='ABOUT_TAB']//div[@class='ui_column  '][2]//div[@class='ui_columns is-mobile']/div[1]/div[2]/span//*[name()='svg' and @class='AZd6Ff4E']")
            hotelClass = hotelClassValue.get_attribute("aria-label")
            hotelClass = float(hotelClass[0]) + float(hotelClass[2])/10
        except:
            hotelClass = 0
        
        try:
            locationStars = driver.find_element_by_xpath("//*[@id='ABOUT_TAB']/div[2]/div[1]/div[2]/span")
            locationRatingValue = locationStars.get_attribute("class")
            locationRating = getRatingValue(locationRatingValue)
    
            cleanlinessStars = driver.find_element_by_xpath("//*[@id='ABOUT_TAB']/div[2]/div[1]/div[3]/span")
            cleanlinessRatingValue = cleanlinessStars.get_attribute("class")
            cleanlinessRating = getRatingValue(cleanlinessRatingValue)

            serviceStars = driver.find_element_by_xpath("//*[@id='ABOUT_TAB']/div[2]/div[1]/div[4]/span")
            serviceRatingValue = serviceStars.get_attribute("class")
            serviceRating = getRatingValue(serviceRatingValue)

            valueStars = driver.find_element_by_xpath("//*[@id='ABOUT_TAB']/div[2]/div[1]/div[5]/span")
            valueRatingValue = valueStars.get_attribute("class")
            valueRating = getRatingValue(valueRatingValue)
        except:
            locationRating = 0
            cleanlinessRating = 0
            serviceRating = 0
            valueRating = 0
        
        try:
            descriptionDiv = driver.find_element_by_xpath('//*[@id="ABOUT_TAB"]/div[2]/div[1]/div[7]/div/div[1]')
            description = descriptionDiv.text
            if not description:
                descriptionDiv = driver.find_element_by_xpath('//*[@id="ABOUT_TAB"]/div[2]/div[1]/div[6]/div/div[1]')
                description = descriptionDiv.text
            if not description:
                descriptionDiv = driver.find_elements_by_xpath('//*[@id="ABOUT_TAB"]/div[3]/div[1]/div[6]/div/div[1]/div/p')
                for paragraph in descriptionDiv:
                    description = description + paragraph + " "
        except:
            description = "NO DESCRIPTION"
    
        try:
            button = driver.find_element_by_xpath("//*[@id='ABOUT_TAB']/div[2]/div[2]/div[1]/div[3]/div")
            button.click()
            amenitiesList = driver.find_elements_by_xpath("//*[@id='BODY_BLOCK_JQUERY_REFLOW']/div[@class='_32oTjHgM']/div/div/div/div[3]/div[1]/div/div")
            for amenity in amenitiesList:
                amenities.append(amenity.text)
        except:
            try:
                amenitiesList = driver.find_elements_by_xpath("//*[@id='ABOUT_TAB']/div[2]/div[2]/div[1]/div[2]/div")
                for amenity in amenitiesList:
                     amenities.append(amenity.text)
            except:
                print("no amenities")
        return titleText, locationText, hotelClass, int(reviewsNumberTmp), averageRating, locationRating, cleanlinessRating, serviceRating, valueRating, description, amenities
    except:
        print("NO")

PATH = "C:\chromedriver.exe"
driver = webdriver.Chrome(PATH)

currentpage = "https://www.tripadvisor.com/Search?q=slovenia&searchSessionId=0245589C18F1D6164283105A54A805491606936354720ssid&sid=E1083FC871454FBF51FACA5A442B92FF1606936367578&blockRedirect=true&ssrc=h&geo=274862&rf=9"

listOfHotels = []
hotelsInformation = []

for i in range(34):
    print(i)
    driver.get(currentpage + "&o=" + str(i * 30))
    time.sleep(3)
    hotels = driver.find_elements_by_xpath("//a[@class='review_count']")
    for hotel in hotels:
        listOfHotels.append(hotel.get_attribute('href')[:-8])
    for i in range(len(listOfHotels)):
        hotelsInformation.append(find_information(listOfHotels[i]))
    listOfHotels.clear()

hotelsInformation = list(filter(None, hotelsInformation))

filename = "hotels.csv"
fields = ["Name", "Location", "Hotel Class", "Number of reviews", "Average rating", "Location Rating", "Cleanliness Rating", "Service Rating", "Value Rating", "Description", "Amenities"]
with open(filename, 'w', encoding="utf-8") as csvfile:  
    csvwriter = csv.writer(csvfile)   
    csvwriter.writerow(fields)   
    csvwriter.writerows(hotelsInformation)
print("DONE, EXCEL CREATED")
driver.quit()