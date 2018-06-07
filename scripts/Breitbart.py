import requests
from bs4 import BeautifulSoup
import re
#The basics
import numpy as np
import pandas as pd

#Get them web sites
import requests

#Make sure slenium works
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

#Start the google driver
driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
#For inserting articles into Mongodb
from pymongo import MongoClient
#Starts url at politics section
url_rueters = 'http://www.breitbart.com/big-government/'
response = requests.get(url_rueters)
#functions
def get_case_links_from_html(html):
    """
    gets list of links from breitbart
    """
    soup = BeautifulSoup(html, 'lxml')
    return list(set(article['href'] for article in soup.find_all('a', class_="tumbnail-url")))

def get_case_links_from_page(page_num, driver):
    url = url_generator(page_num)
    driver.get(url)
    time.sleep(1)
    html = driver.page_source
    return get_case_links_from_html(html)
#starts iterting through pages
current_url = 'http://www.breitbart.com/big-government/'
next_url    = 'http://www.breitbart.com/big-government/page/2/'

def url_generator(page_num):
    return 'http://www.breitbart.com/big-government/page/{}/'.format(page_num)
#pipeline for getting links
driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
driver.get(current_url)
time.sleep(1)
pages = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
breitbart_articles = []
soup = BeautifulSoup(driver.page_source, 'lxml')
more_breitbart_articles = []
for article in soup.find_all('a', class_="thumbnail-url"):
    link = article['href']
    breitbart_articles.append(link)
    #article_link = article_link[5:]
for x in pages:
    driver.get(url_generator(x))
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    for article in soup.find_all('a', class_="thumbnail-url"):
        link = article['href']
        more_breitbart_articles.append(link)
#functions
def get_breitbart_article(url):
    #makes the request
    page = requests.get(url)
    html = page.text
    return html

def parse_breitbart_article(html):
    #BeautifulSoup the page
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h1').text
    body = soup.find('div', class_='entry-content').text

    article = {
        'title': title,
        'body': body,
        'source': 'Breitbart',
        'num_source': 3
    }

    return article

def get_parsed_article_from_link(url):
    #runs functions on each link
    return parse_breitbart_article(get_breitbart_article(url))
#figures out how to convert links
for x in breitbart_articles[:15]:
    y = 'http://www.breitbart.com' + x
    breitbart_articles.append(y)
#get unique list
breitbart_articles = list(set(breitbart_articles))
#phase 1 of first page pipeline
breitbart_list_o_articles = []
breitbart_problem_articles = []
for text in breitbart_articles:
    try:
        art = get_parsed_article_from_link(text.encode())
        breitbart_list_o_articles.append(art)

    except:
        print("Problem processing url " + text)
        problem = text
        breitbart_problem_articles.append(problem)
    time.sleep(3)
#phase 2 for first page
for x in breitbart_problem_articles:
    try:
        driver.get(x)
        time.sleep(3)
        soupy = BeautifulSoup(driver.page_source, 'lxml')
        title = soupy.find('h1', class_='headline_2zdFM').text
        body = soupy.find('div', class_='body_1gnLA').text

        articley = {
            'title': title,
            'body': body,
            'source': 'Breitbart',
            'num_source': 3
        }
        breitbart_list_o_articles.append(articley)
    except:
        pass

#get unique list
more_breitbart_articles = list(set(more_breitbart_articles))

#phase 1 for rest of pages
more_breitbart_list_o_articles = []
more_breitbart_problem_articles = []
for text in more_breitbart_articles:
    try:
        art = get_parsed_article_from_link(text.encode())
        more_breitbart_list_o_articles.append(art)

    except:
        print("Problem processing url " + text)
        problem = text
        more_breitbart_problem_articles.append(problem)
    time.sleep(3)
#phase 2 for rest
for x in more_breitbart_problem_articles:
    try:
        driver.get(x)
        time.sleep(3)
        soupy = BeautifulSoup(driver.page_source, 'lxml')
        title = soupy.find('h1', class_='headline_2zdFM').text
        body = soupy.find('div', class_='body_1gnLA').text

        articley = {
            'title': title,
            'body': body,
            'source': 'Breitbart',
            'num_source': 3
        }
        more_breitbart_list_o_articles.append(articley)
    except:
        pass

#starts client in Mongodb
client = MongoClient()
biased_news = client.project5.biased_news
#creates event and loads articles into Mongodb
db = client.events
biased_news = db.biased_news
biased_news.insert_many(breitbart_list_o_articles)
biased_news.insert_many(more_breitbart_list_o_articles)
