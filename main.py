from selenium import webdriver
from bs4 import BeautifulSoup
from time import gmtime, strftime, sleep
import requests
import re
import json

url_str = input("Enter the product category you want to search for: ")

words = url_str.split()
root_url = "https://www.amazon.com"

driver = webdriver.Chrome()

def getLinks (f, url) :
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    product_image_containers = soup.find_all("span", {"data-component-type": "s-product-image"})
    for container in product_image_containers:
        f.write(root_url + container.find("a")["href"] + "," + words[0] + "\n")
    print('Sleeping ...')
    sleep(2)
    next_page = soup.find("a", {"class": "s-pagination-next"})
    if next_page:
        print('Fetching next page')
        getLinks(f, root_url + next_page["href"])
    else:
        print('End')

for word in words:
    f = open("product_lists_" + word + "_" + strftime("%Y-%m-%d-%H-%M-%S", gmtime()) + ".csv", "w", encoding='utf-8')
    getLinks(f, root_url + "/s?k=" + word)
    sleep(4)