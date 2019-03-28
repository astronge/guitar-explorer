from request import simple_get
from bs4 import BeautifulSoup, element
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import requests
import os
import time
import sys

project = os.path.dirname(os.path.abspath(__file__))

def get_brand_urls():
    # set base url 
    url = "https://www.musiciansfriend.com/electric-guitars"

    # start new Firefox session
    driver = webdriver.Firefox(executable_path=r"C:\Users\Aaron\geckodriver.exe")
    driver.implicitly_wait(5)
    driver.get(url)

    # click link to display full list of brands
    expand_brand = driver.find_element_by_class_name("load-all-refinements--link")
    expand_brand.click()
    WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.CLASS_NAME, "facets.radio.overflow-facet.loaded")))
    src = driver.page_source

    # get soup 
    soup = BeautifulSoup(src, "html.parser")

    # create list to hold brand dictionaries
    brand_list = []

    # create a list from each brand"s object
    brand_container = soup.find("ul", id="facet_200000")
    brands = brand_container.find_all("a")

    # iterate over each brand"s object to grab brand name and product count
    for brand in brands:

        # get brand product count
        brand_text = brand.get_text()
        count_raw = brand_text.rsplit("\xa0", 1)[1]
        count = int(count_raw.replace("(", "").replace(")", ""))

        # get brand name
        brand_name_url = brand.get("href")
        brand_name = brand_name_url.replace("/electric-guitars/", "")

        # get brand ID (for URL)
        brand_id_list = brand.get("rel")
        brand_id = brand_id_list[0]

        # put all into dictionary
        brand_list.append({"brand" : brand_name, "count" : count, "id" : brand_id})

    print(brand_list)
    return brand_list


def get_guitar_urls(brand_list):

    # get query string for brand product pages
    url = "https://www.musiciansfriend.com/electric-guitars"
    raw_html = simple_get(url)
    soup = BeautifulSoup(raw_html, "html.parser")
    query_string_soup = soup.find("var", id="queryString")
    query_string = query_string_soup.get_text()

    # define the parts of the URL to gather guitar URLs from
    url_stem = "https://www.musiciansfriend.com/electric-guitars/"
    url_part1 = query_string + "#pageName=category-page&N=500002+"
    url_part2 = "&Nao="
    url_part3 = "&recsPerPage=30&profileCountryCode=US&profileCurrencyCode=USD"

    # iterate through brands in the list
    for brand in brand_list:
        # check if guitar_urls file  
        file_name = "/data/guitar_urls/guitar_urls_" + brand["brand"] + ".txt"
        file_path = project + file_name
        if os.path.exists(file_path):
                os.remove(file_path)
                print("Removed /data/guitar_urls/guitar_urls" + brand["brand"] + ".txt file")

        # set counter
        i = 0

        # continue looking for new pages while the count is less than number of products
        while i < brand["count"]:
            url_stem = "https://www.musiciansfriend.com/electric-guitars/" + brand["brand"]
            url_part1 = query_string + "+" + brand["id"]
            url_part2 = "&Nao=" + str(i)
            url_part3 = "&recsPerPage=30&profileCountryCode=US&profileCurrencyCode=USD"

            # assemble page URL for brand and soup
            brand_url = url_stem + url_part1 + url_part2 + url_part3
            raw_html = simple_get(brand_url + "\n--------------------------\n")
            soup = BeautifulSoup(raw_html, "html.parser")
            products = soup.find_all("li", class_ = "product-container")
            
            for product in products:
                product_url_raw = product.find("a")
                product_url = "https://www.musiciansfriend.com" + product_url_raw.get("href")
                image_raw = product.find("img")
                image_url = image_raw.get("data-original")
                
                #log_file.write(product_url + "\n")

                # append new URL to file defined at beginning of function
                guitar_url_data = open(file_path, "a")
                guitar_url_data.write(image_url + "\n")
                guitar_url_data.write(product_url + "\n")
    
            # increment to get next url
            i = i + 30

            # sleep for random interval before next call
            random = randint(2, 10)
            print("Sleeping for: " + str(random) + " seconds before next call")
            for k in range (random, 0, -1):
                sleep(1)


def get_guitar_data():

    directory = "/data/guitar_urls/"
    file_path = project + directory

    for file_name in os.listdir(file_path):

        brand_file = file_name.replace(".txt", "")
        brand = brand_file.replace("guitar_urls_", "")
        file_name_path = file_path + file_name

        # starting id for first JSON entry
        json_id = 1
        count = 1

        # variable for image or page url
        is_image = 1
        page_url = ""
        image_url = ""

        # create dictionary to hold the guitar data
        guitars = {}

        with open(file_name_path) as guitar_urls:
            for url in guitar_urls:
                if is_image == 1:
                    image_url = url
                    is_image = 2
                    continue
                else:
                    page_url = url
                    is_image = 1
                    # pause for random period before next call
                    random = randint(2, 10)
                    print("Sleeping for: " + str(random) + " seconds before next call")
                    for i in range (random, 0, -1):
                        sleep(1)
                    print(str(count) + ": " + url)
                    
                    count = count + 1

                    raw_html = simple_get(url)
                    
                    soup = BeautifulSoup(raw_html, "html.parser")

                    # dictionary to hold the data
                    features = {}

                    try:
                        # get manufacturer and product name
                        manufacturer_product = soup.find_all("var", class_="hidden fn") 
                        manufacturer_product_text = manufacturer_product[0].get_text()
                        manufacturer_product_split = manufacturer_product_text.split(None, 1)
                        manufacturer = manufacturer_product_split[0]
                        product = manufacturer_product_split[1]

                        # get product ID
                        product_sku = soup.find_all("var", class_="hidden sku") 
                        product_id = product_sku[0].get_text()

                        # add manufacturer and product info into features dictionary
                        features.update({"Manufacturer" : manufacturer})
                        features.update({"Product" : product})
                        features.update({"Product ID" : product_id})

                        # get price
                        price_raw = soup.find_all("span", class_="productPrice")[0]
                        price_text_whole = price_raw.get_text()
                        price_text_split = price_text_whole.split("$")
                        price_text = price_text_split[1]
                        price_clean = price_text.replace(",","")
                        price = float(price_clean)

                        # add price to features
                        features.update({"Price" : price})

                        # get all features with flexibility for inconsistency in DOM
                        if len(soup.find_all("div", class_="specs")) > 1:
                            spec_list = soup.find_all("div", class_="specs")[1]
                        elif soup.find_all("div", class_="specs") == 1: 
                            spec_list = soup.find_all("div", class_="specs")[0]
                        else:
                            continue

                        # create list of feature groupings
                        headers = spec_list.find_all("strong")
                        if headers:  
                            header_text = [header.get_text() for header in headers]
                        else:
                            header_text = []

                        # isolate the lists for each feature grouping
                        if header_text:
                            if spec_list.select("p"):
                                lists = spec_list.select("p")
                            elif spec_list.select("ul"):
                                lists = spec_list.select("ul")
                            else:
                                continue
                        else:
                            lists = []

                        # add each feature grouping and associated features
                        i = 0
                        if lists: 
                            for ul in lists:
                                if header_text:
                                    features[header_text[i]] = {}
                                    # split subfeature into key/value pairs.  
                                    # if colon separation exists, use that, otherwise use first space
                                    for li in ul:
                                        if type(li) == element.Tag:
                                            if ":" in li.get_text():
                                                key_value = li.get_text().split(":")
                                                if len(key_value) > 1:
                                                    key = key_value[0].lstrip()
                                                    value = key_value[1].lstrip()
                                                    features[header_text[i]].update({key : value})
                                                else:
                                                    print("no feature value")
                                            elif li.get_text().isspace():
                                                print("no feature value")
                                            else:
                                                key_value = li.get_text().split(" ", 1)
                                                if len(key_value) > 1:
                                                    key = key_value[0].lstrip()
                                                    value = key_value[1].lstrip()
                                                    features[header_text[i]].update({key : value})
                                                else:
                                                    print("no feature value")
                                        else:
                                            continue
                                    i = i+1
                                else:
                                    continue
                        else: 
                            continue
                        
                        # add page and image urls to features
                        features.update({"page_url" : page_url})
                        features.update({"image_url" : image_url})

                        # add set of features to master dictionary
                        guitars.update({json_id : features})
                    
                    except:
                        continue

                # load json and write it to file
                guitar_data_file = "/data/guitar_data/guitar_data_" + brand + ".json"
                guitar_data_file_path = project + guitar_data_file
                guitars_json = json.dumps(guitars)
                guitar_data = open(guitar_data_file_path, "w")
                guitar_data.write(guitars_json)
                guitar_data.close()
                
                # increment json_id to give next URL results next ID
                json_id = json_id + 1