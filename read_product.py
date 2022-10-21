from selenium import webdriver
from bs4 import BeautifulSoup
from time import gmtime, strftime, sleep
import requests
import re
import json
import uuid

url = "https://www.amazon.com/sspa/click?ie=UTF8&spc=MTo3MTYwNTk0Nzk3Mzc1OTM4OjE2NjYzMTgxNTY6c3BfYXRmOjIwMDA5NDk4NDkxNDA5ODo6MDo6&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&url=%2FNerve-Regen-Formula-Advanced-Discomfort%2Fdp%2FB09G6KP5TC%2Fref%3Dsr_1_1_sspa%3Fkeywords%3Dsupplement%26qid%3D1666318156%26qu%3DeyJxc2MiOiI4LjAyIiwicXNhIjoiNy43OSIsInFzcCI6IjcuMTMifQ%253D%253D%26sr%3D8-1-spons%26psc%3D1%26smid%3DA27GX2M01OSNPO"

driver = webdriver.Chrome()

driver.get(url)

data = {
    "url": url
}

soup = BeautifulSoup(driver.page_source, 'html.parser')

print("reading...")

data["title"] = soup.find("span", {"id": "productTitle"}).getText().strip()

price = soup.find("div", {"id": "corePrice_desktop"})
data["price"] = price.find("span", {"class": "a-price"}).find("span", {"class": "a-offscreen"}).getText()

def findFeature(feature) :
    n = feature.find("span", {"class": "a-text-bold"})
    v = feature.find("span", {"class": "a-size-base"})
    return [n.getText() if n else None, v.getText() if v else None]
features = soup.find("div", {"id": "productOverview_feature_div"})
features = map(findFeature, features.find_all("tr"))
data["features"] = list(features)

def findImportant(important) :
    n = important.find("h4")
    v = map(lambda p: p.getText(), important.find_all("p"))
    return [n.getText() if n else None, "\n".join([x for x in v if x])]
important = soup.find("div", {"id": "important-information"})
important = map(findImportant, important.find_all("div", {"class": "a-section"}))
data["important-information"] = list(important)

json_object = json.dumps(data, indent=4)

print("saving...")

with open("products/" + str(uuid.uuid4()) + ".json", "w") as outfile:
    outfile.write(json_object)


print("saved")