import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq



class monsterJobScrapper:

    def createUrl(self, jobTitle, location):
        test_url = "https://www.monsterindia.com/search/{}-jobs-in-{}?searchId=66e9a389-64c6-4521-812a-e6f01ce88b39".format(jobTitle, location)
        return test_url

    def get_webPage(self, test_url):
        uClient = uReq(test_url)
        monsterPage = uClient.read()
        uClient.close()
        monster_html = bs(monsterPage, "html.parser")
        bigboxes = monster_html.findAll("div", {"class": "card-apply-content"})
        return bigboxes