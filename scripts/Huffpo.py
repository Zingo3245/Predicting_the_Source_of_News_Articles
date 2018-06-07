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


def get_case_links_from_html(html):
#BeautifulSoups the article links
    soup = BeautifulSoup(html, 'lxml')
    return list(set('https://www.huffingtonpost.com' + article['href'] for article in soup.find_all('a', class_="card__link yr-card-headline")))

def get_case_links_from_page(page_num, driver):
#cycles through the pages nand gets the links
    url = url_generator(page_num)
    driver.get(url)
    time.sleep(1)
    html = driver.page_source
    return get_case_links_from_html(html)

def get_article(url):
#Sends request for url
    html = requests.get(url).text
    return html

def parse_article(html):
#BeautifulSoups the article
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h1', class_='headline__title').text
    body = soup.find('div', class_='entry__text js-entry-text yr-entry-text').text

    article = {
        'title': title,
        'body': body,
        'source': 'Huffington Post',
        'num_source': 1
    }

    return article

def get_parsed_article_from_link(url):
#Runs the previous two functions on the url
    return parse_article(get_article(url))
#Starts the url chain
current_url = 'https://www.huffingtonpost.com/section/politics'
next_url    = 'https://www.huffingtonpost.com/section/politics?page=2'

def url_generator(page_num):
#iters through the pages
    return 'https://www.huffingtonpost.com/section/politics?page={}'.format(page_num)
'''
#Runs selenium on the huff po politics section
driver = driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
driver.get('https://www.huffingtonpost.com/section/politics')
time.sleep(1)
soup = BeautifulSoup(driver.page_source, 'lxml')
#gets the list of links from the first page
first_articles = []
for article in soup.find_all('a', class_="card__link yr-card-headline"):
        link = 'https://www.huffingtonpost.com' + article['href']
        first_articles.append(link)
#Get unique links
first_articles = list(set(first_articles))
#iters through the subsequent pages and gets the links
driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
driver.get(current_url)
time.sleep(1)
pages = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
more_articles = []
for x in pages:
    driver.get(url_generator(x))
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    for article in soup.find_all('a', class_="card__link yr-card-headline"):
        link = 'https://www.huffingtonpost.com' + article['href']
        more_articles.append(link)

#phase 1: uses request to try to BeautifulSoup links
list_o_articles = []
problem_articles = []
for text in first_articles[5:]:
    #print(text)
    try:
        art = get_parsed_article_from_link(text.encode())
        list_o_articles.append(art)

    except:
        print("Problem processing url " + text)
        problem = text
        problem_articles.append(problem)
    time.sleep(2)
#phase 2: uses selenium to go through links
driver = driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
for x in problem_articles:
    try:
        driver.get(x)
        time.sleep(3)
        soupy = BeautifulSoup(driver.page_source, 'lxml')
        title = soupy.find('h1', class_='headline__title').text
        body = soupy.find('div', class_='entry__text js-entry-text yr-entry-text').text

        articley = {
            'title': title,
            'body': body,
            'source': 'Huffington Post',
            'num_source': 1
        }

        list_o_articles.append(articley)
    except:
        pass
'''
#Gets unique links for more articles
more_articles = ['https://www.huffingtonpost.com/entry/trump-scottish-golf-resort-pays-women-less-than-men_us_5b08ca29e4b0802d69cb4d37',
 'https://www.huffingtonpost.com/entry/donald-trump-denounces-rumors-about-melania-trumps-absence_us_5b17e8cde4b0734a9939af13',
 'https://www.huffingtonpost.com/entry/trump-phone-security_us_5b049d53e4b0784cd2af5486',
 'https://www.huffingtonpost.com/entry/immigrant-detention-courts_us_5b0725f0e4b0802d69c958d3',
 'https://www.huffingtonpost.com/entry/wendy-vitter-abortion-trump-judge_us_5afd8918e4b06a3fb50e5c68',
 'https://www.huffingtonpost.com/entry/one-third-americans-trump-draining-swamp_us_5b0462d2e4b0784cd2af148e',
 'https://www.huffingtonpost.com/entry/fbi-wiretaps-putin-ally-trump-jr_us_5b08bf56e4b0568a880b7859',
 'https://www.huffingtonpost.com/entry/new-hampshire-voter-fraud-investigation-trump_us_5b0ef7d3e4b0be10a488181b',
 'https://www.huffingtonpost.comhttps://www.huffingtonpost.com/topic/2018-elections',
 'https://www.huffingtonpost.com/entry/china-tariffs-us-hold_us_5b018af2e4b0a046186d214f',
 'https://www.huffingtonpost.com/entry/diane-black-porn-school-shootings_us_5b16e871e4b0734a9938474d',
 'https://www.huffingtonpost.com/entry/donald-trump-tomi-lahren-tweet_us_5b064e26e4b07c4ea104b9bf',
 'https://www.huffingtonpost.com/entry/donald-trump-says-he-wishes-he-hadnt-picked-jeff-sessions-as-attorney-general_us_5b0e9e01e4b0fdb2aa587e8b',
 'https://www.huffingtonpost.com/entry/houston-police-chief-says-he-is-sick-of-inaction-over-gun-control_us_5b003eefe4b0a046186c4346',
 'https://www.huffingtonpost.com/entry/chrissy-teigen-donald-trump-twitter-blocked_us_5b066140e4b07c4ea104cd97',
 'https://www.huffingtonpost.com/entry/president-obama-mouse-buckingham-palace_us_5b1803c2e4b0734a9939fd7c',
 'https://www.huffingtonpost.com/entry/emails-bears-ears-national-monument-review-comment-period_us_5afd7e8fe4b06a3fb50e47f0',
 'https://www.huffingtonpost.com/entry/roger-stone-prepared-for-conjured-up-mueller-indictment_us_5b020043e4b0463cdba39f60',
 'https://www.huffingtonpost.com/entry/report-manaforts-former-son-in-law-cuts-plea-deal-to-cooperate-with-government_us_5afe45c8e4b07309e05660e5',
 'https://www.huffingtonpost.com/entry/catholic-hospitals-refuse-to-treat_us_5b06c82fe4b05f0fc8458db3',
 'https://www.huffingtonpost.com/entry/house-democrats-announced-internship-for-students-impacted-by-gun-violence_us_5b06ee0fe4b05f0fc846005f',
 'https://www.huffingtonpost.com/entry/paul-manafort-jail-prediction_us_5b178195e4b0599bc6de33e8',
 'https://www.huffingtonpost.com/entry/trump-contradicts-himself-on-kim-jong-un-letter_us_5b11f438e4b0d5e89e1fc885',
 'https://www.huffingtonpost.com/entry/garry-kasparov-aeroflot-trump-russian-connections_us_5b0341fbe4b0a046186efb9b',
 'https://www.huffingtonpost.com/entry/jim-carey-painting-slams-kent-state-kaitlin-bennett_us_5b00b8f0e4b07309e058fed9',
 'https://www.huffingtonpost.com/entry/roseanne-barr-valerie-jarrett_us_5b0d6e0de4b0fdb2aa571448',
 'https://www.huffingtonpost.com/entry/cynthia-nixon-mta-subway-ads-andrew-cuomo_us_5afda284e4b0a59b4e019369',
 'https://www.huffingtonpost.com/entry/kevin-mccarthy-cnn-white-house_us_5b140c89e4b010565aacd0a6',
 'https://www.huffingtonpost.com/entry/trump-to-host-ramadan-dinner_us_5b140961e4b0d5e89e2089b7',
 'https://www.huffingtonpost.com/entry/trump-more-abortion-curbs-susan-b-anthony-list_us_5b052039e4b07c4ea1033978',
 'https://www.huffingtonpost.com/entry/melania-trump-tweet_us_5b0f065fe4b03368a94e2be9',
 'https://www.huffingtonpost.com/entry/twitter-roars-over-trump-melanie-mistake_us_5b009a5be4b0463cdba2cc37',
 'https://www.huffingtonpost.com/entry/super-pacs-that-meddled-in-west-virginias-senate-primary-didnt-receive-a-penny-from-west-virginians_us_5b01fd3fe4b07309e059c8f6',
 'https://www.huffingtonpost.com/entry/kevin-hart-morning-person_us_5b16a68ae4b081422e210783',
 'https://www.huffingtonpost.com/entry/veterans-group-blasts-trump-memorial-day-remark-most-inappropriate-ever_us_5b0c82dbe4b0fdb2aa55f558',
 'https://www.huffingtonpost.com/entry/farm-bill-food-stamps_us_5afef4dfe4b07309e0579452',
 'https://www.huffingtonpost.com/entry/saudi-arabia-problem-islam-actually-tyranny_us_5b087360e4b0568a880b6662',
 'https://www.huffingtonpost.com/entry/trumps-lawyers-argue-he-cant-obstruct-justice-because-hes-president_us_5b12ebc1e4b0d5e89e2020e3',
 'https://www.huffingtonpost.com/entry/jimmy-kimmel-donald-trump-santa-fe-shooting_us_5affb5dbe4b07309e0581cc9',
 'https://www.huffingtonpost.com/entry/trump-grants-alice-marie-johnson-clemency-kim-kardashian_us_5b16d73ae4b09578259c521e',
 'https://www.huffingtonpost.com/entry/mueller-obstruction-probe-ending-september_us_5b01d8f7e4b0a046186d51d5',
 'https://www.huffingtonpost.com/entry/farm-bill-freedom-caucus_us_5afde293e4b0a59b4e01f4e7',
 'https://www.huffingtonpost.com/entry/trump-roseanne-tweet-snark_us_5b0ed269e4b0802d69d09f80',
 'https://www.huffingtonpost.com/entry/jeffrey-sachs-slams-delusional-psychopathic-trump_us_5b11e510e4b0d5e89e1fc756',
 'https://www.huffingtonpost.com/entry/robert-wilkie-va-secretary_us_5afef7a8e4b0a046186b2a0a',
 'https://www.huffingtonpost.com/entry/republicans-concern-pruitt-votes-say-otherwise_us_5b181c34e4b0734a993a32aa',
 'https://www.huffingtonpost.com/entry/donald-trump-cancels-summit-kim-jong-un_us_5b06c1d9e4b07c4ea105b0f0',
 'https://www.huffingtonpost.com/entry/arizona-voter-registration_us_5b15a536e4b014707d2758ea',
 'https://www.huffingtonpost.com/entry/giuliani-mueller-trump-fbi-source_us_5b032010e4b07309e05b3820',
 'https://www.huffingtonpost.com/entry/ryan-zinke-reel-back-critics-grand-pivot-conservation_us_5b086c78e4b0fdb2aa538b3f',
 'https://www.huffingtonpost.com/entry/vickers-cunningham-pays-kids-for-marrying-white_us_5aff9cfee4b0a046186baa8d',
 'https://www.huffingtonpost.com/entry/eric-trump-life-got-exponentially-worse_us_5b161844e4b0129b529d57d3',
 'https://www.huffingtonpost.com/entry/mike-pompeo-north-korea-dinner_us_5b0fae33e4b05ef4c22ae7b7',
 'https://www.huffingtonpost.com/entry/lauren-arthur-democrat-missouri-special-election-senate_us_5b175388e4b09578259cc336',
 'https://www.huffingtonpost.com/entry/giuliani-trump-russia-collusion_us_5afd206ae4b06a3fb50d92d9',
 'https://www.huffingtonpost.com/entry/house-republicans-report-progress-immigration-deal_us_5b05d923e4b07c4ea1049116',
 'https://www.huffingtonpost.com/entry/ivanka-gets-5-china-trademarks-as-president-works-zte-deal_us_5b0a07eee4b0568a880c0a0d',
 'https://www.huffingtonpost.com/entry/donald-trump-samantha-bee_us_5b118337e4b0d5e89e1f8b1c',
 'https://www.huffingtonpost.com/entry/anti-muslim-twitter-troll-amy-mek-mekelburg_us_5b0d9e40e4b0802d69cf0264',
 'https://www.huffingtonpost.com/entry/democrats-push-included-classified-briefing-fbi-informant_us_5b058d4fe4b07c4ea1042f94',
 'https://www.huffingtonpost.com/entry/stephanie-kelton-economy-washington_us_5afee5eae4b0463cdba15121',
 'https://www.huffingtonpost.com/entry/initial-talks-for-trump-putin-summit_us_5b1226f1e4b0d5e89e1fcf14',
 'https://www.huffingtonpost.com/entry/philadelphia-eagles-fox-news-propaganda-prayer-photo_us_5b16982de4b081422e20e40a',
 'https://www.huffingtonpost.com/entry/donald-trump-may-jobs-report-tweet_us_5b1155ebe4b02143b7cbe24c',
 'https://www.huffingtonpost.com/entry/ryan-zinke-wildlife-conservation-montana-david-spady_us_5b153d81e4b010565aadf457',
 'https://www.huffingtonpost.com/entry/trump-scare-immigrants-not-working_us_5b186744e4b0734a993aa224',
 'https://www.huffingtonpost.com/entry/dinesh-dsouza-pardoned-by-donald-trump_us_5b0ff689e4b0fcd6a83449dd',
 'https://www.huffingtonpost.com/entry/tulsi-gabbard-syria_us_5b057ab8e4b0784cd2b0653d',
 'https://www.huffingtonpost.com/entry/senators-reach-bipartisan-deal-sexual-harassment_us_5b0452cfe4b0740c25e5ecc6',
 'https://www.huffingtonpost.com/entry/california-primary-election-results-this-is-going-to-take-a-while_us_5b17488de4b0599bc6de196e',
 'https://www.huffingtonpost.com/entry/lady-gaga-a-star-is-born_us_5b182054e4b09578259e6b92',
 'https://www.huffingtonpost.com/entry/south-dakota-governor-race_us_5b156763e4b02143b7cee66a',
 'https://www.huffingtonpost.com/entry/melania-trump-reappears-gold-star-reception_us_5b163248e4b093ac33a14d87',
 'https://www.huffingtonpost.com/entry/top-scott-pruitt-aide-resigns-from-epa_us_5b183350e4b09578259e974a',
 'https://www.huffingtonpost.com/entry/kirstjen-nielsen-russian-interference_us_5b043763e4b0c0b8b23e99a7',
 'https://www.huffingtonpost.com/entry/trump-prison-reform-tweets_us_5aff37f8e4b07309e057f6a9',
 'https://www.huffingtonpost.com/entry/oliver-north-school-shootings_us_5b018dece4b0a046186d22be',
 'https://www.huffingtonpost.com/entry/trump-opens-door-us-gun-industry-sell-firearms-abroad_us_5b071e1ce4b0784cd2b2e65f',
 'https://www.huffingtonpost.com/entry/supreme-court-arkansas-restrict-medical-abortions_us_5b0d6691e4b0fdb2aa5707cf',
 'https://www.huffingtonpost.com/entry/elizabeth-warren-patty-murray-trump-global-health-adviser_us_5afe3278e4b07309e05659e2',
 'https://www.huffingtonpost.com/entry/the-georgia-gop-governor-primary-is-all-about-the-culture-war-and-three-other-things-to-watch-on-tuesday_us_5b032b3ee4b0a046186ed9c4',
 'https://www.huffingtonpost.com/entry/vicente-fox-donald-trump-immigrants-animals_us_5afd373ce4b0779345d6045a',
 'https://www.huffingtonpost.com/entry/california-gubernatorial-primary_us_5b15b90de4b0129b529d2fb2',
 'https://www.huffingtonpost.com/entry/trump-power-supreme-court-showdown_us_5b16e958e4b09578259c7adc',
 'https://www.huffingtonpost.com/entry/bill-clinton-monica-lewinsky_us_5b156e55e4b0d5e89e223ff5',
 'https://www.huffingtonpost.com/entry/onion-michael-cohen-cease-and-desist_us_5b037f77e4b0a046186f13b3',
 'https://www.huffingtonpost.com/entry/dean-heller-paid-his-social-media-influencer-son-more-than-50000-out-of-his-campaign-account_us_5afe02c6e4b0a0461869d674',
 'https://www.huffingtonpost.com/entry/white-nationalist-charlottesville-elected-local-gop-office_us_5b1698b7e4b074b9e089f1f7',
 'https://www.huffingtonpost.com/entry/bill-clinton-donald-trump-impeachment_us_5b142ad3e4b0d5e89e2098f3',
 'https://www.huffingtonpost.com/entry/trump-mueller-midterms_us_5b0d391ee4b0802d69ce5a74',
 'https://www.huffingtonpost.com/entry/michelle-obama-cover-memoir-becoming_us_5b06c7f2e4b05f0fc8458cb4',
 'https://www.huffingtonpost.com/entry/puerto-rico-governor-hurricane-maria-stats_us_5b1168b8e4b0d5e89e1f5098',
 'https://www.huffingtonpost.com/entry/white-house-aide-out-mocking-mccain_us_5af5790be4b00d7e4c19b485',
 'https://www.huffingtonpost.com/entry/so-states-ban-bump-stocks-now-how-do-they-enforce_us_5afef574e4b018ba2f83c189',
 'https://www.huffingtonpost.com/entry/trump-rules-to-block-funds-at-clinics-providing-abortion_us_5afe665de4b0a046186a02d6',
 'https://www.huffingtonpost.com/entry/lawmaker-introduces-crowdfunding-bill-border-wall_us_5b036c8be4b0a046186f0e6f',
 'https://www.huffingtonpost.com/entry/human-trafficking-banking-bill-sex-workers_us_5b045577e4b0740c25e5efd1',
 'https://www.huffingtonpost.com/entry/best-netflix-shows-movie-june_us_5b16c6a4e4b0734a993809e8',
 'https://www.huffingtonpost.com/entry/trumps-pardons-message-to-allies-russia-investigation_us_5b103d5ee4b0a1f9f180d1fb',
 'https://www.huffingtonpost.com/entry/kris-kobach-defends-parade-appearance-with-replica-machine-gun_us_5b163808e4b093ac33a155e5',
 'https://www.huffingtonpost.com/entry/beyonc%C3%A9-jay-z-twins-rumi-sir-on-the-run-ii-tour_us_5b1836f5e4b09578259e9b20',
 'https://www.huffingtonpost.com/entry/trey-gowdy-informant-spy_us_5b0dfffde4b0802d69cf6245',
 'https://www.huffingtonpost.com/entry/facebook-disclosure-ads_us_5b16b627e4b0734a9937d94d',
 'https://www.huffingtonpost.com/entry/philadelphia-eagles-white-house-super-bowl-trump_us_5b15c73fe4b0129b529d357f',
 'https://www.huffingtonpost.com/entry/ted-cruz-curse-houston-rockets_us_5b0cee92e4b0568a880df5bd',
 'https://www.huffingtonpost.com/entry/texas-voter-registration-online-update_us_5b03370ee4b0a046186ee9a7',
 'https://www.huffingtonpost.com/entry/alabama-census-undocumented-immigrants_us_5b07028ee4b05f0fc84629a7',
 'https://www.huffingtonpost.com/entry/bishop-michael-curry-joins-christian-march-to-white-house-to-reclaim-jesus_us_5b07261ae4b0fdb2aa51b060',
 'https://www.huffingtonpost.com/entry/josh-holt-begs-from-venezuela-prison_us_5afd706ee4b0779345d676ca',
 'https://www.huffingtonpost.com/entry/red-flag-law-gun-study_us_5b10133ee4b0fcd6a8348d67',
 'https://www.huffingtonpost.com/entry/rudy-giuliani-bronx-cheer-dictionarycom_us_5b0d32d5e4b0568a880e84a3',
 'https://www.huffingtonpost.com/entry/supreme-court-helping-companies-sexual-harassment_us_5b02f3c1e4b0463cdba4c638',
 'https://www.huffingtonpost.com/entry/bank-bill-deregulation-congress_us_5b043b70e4b0c0b8b23ea6cd',
 'https://www.huffingtonpost.com/entry/raucous-press-conference-grills-sanders-on-trump-tower-meeting_us_5b15dd47e4b093ac33a1092d',
 'https://www.huffingtonpost.com/entry/rachel-brosnahan-remembers-aunt-kate-spade-as-beautifully-sensitive_us_5b17e86de4b0599bc6df3141',
 'https://www.huffingtonpost.com/entry/america-poverty-worse-under-trump_us_5b131f08e4b010565aac77bc',
 'https://www.huffingtonpost.com/entry/trump-paris-one-year-anniversary_us_5b107325e4b0d5e89e1e3e78',
 'https://www.huffingtonpost.com/entry/conservative-billionaire-david-koch-steps-down-from-political-business-roles_us_5b169eb5e4b074b9e089fdf1',
 'https://www.huffingtonpost.com/entry/donald-trump-young-and-beautiful_us_5b0ab107e4b0568a880c5d11',
 'https://www.huffingtonpost.com/entry/trump-kim-jong-un-commemorative-coin_us_5b045b9ae4b003dc7e471444',
 'https://www.huffingtonpost.com/entry/everything-donald-trump-jr-doesnt-know-about-meeting_us_5afc5fd4e4b0779345d52258',
 'https://www.huffingtonpost.com/entry/rudy-giuliani-donald-trump-tower_us_5b15f598e4b093ac33a113c8',
 'https://www.huffingtonpost.com/entry/judge-candidate-danny-alvarez-dies_us_5b06aee4e4b05f0fc84557c3',
 'https://www.huffingtonpost.com/entry/house-republicans-daca-immigration-discharge-petition_us_5b18474be4b0599bc6e016a2',
 'https://www.huffingtonpost.com/entry/donald-trump-responds-to-samantha-bee-controversy_us_5b1051e4e4b0e096a4627ee8',
 'https://www.huffingtonpost.com/entry/mexico-not-paying-for-the-wall_us_5b0e09ece4b0568a880f9bda',
 'https://www.huffingtonpost.com/entry/martese-edwards-attempted-murder-charge-white-house_us_5b1783d2e4b0734a9938ade4',
 'https://www.huffingtonpost.com/entry/abc-knew-exactly-what-they-were-getting-with-roseanne_us_5b0db3bbe4b0802d69cf28d4',
 'https://www.huffingtonpost.com/entry/trump-signs-executive-orders-making-it-easier-to-fire-federal-workers_us_5b087a5de4b0568a880b6d36',
 'https://www.huffingtonpost.com/entry/teacher-defeats-kentucky-house-leader_us_5b04c3a2e4b0784cd2af673b',
 'https://www.huffingtonpost.com/entry/fb-justice-department-arrest-allegedspy-china_us_5b15b0c3e4b093ac33a0f27b',
 'https://www.huffingtonpost.com/entry/georgia-republican-primary_us_5b047c28e4b0784cd2af3795',
 'https://www.huffingtonpost.com/entry/school-shooting-gun-laws-poll-santa-fe_us_5b048095e4b07c4ea102c871',
 'https://www.huffingtonpost.com/entry/6-sandy-hook-relatives-fbi-agent-sue-alex-jones-for-defamation_us_5b058f2be4b0784cd2b0aa6e',
 'https://www.huffingtonpost.com/entry/aaron-persky-brock-turner-judge-recalled_us_5b102d65e4b05ef4c22c1b8b',
 'https://www.huffingtonpost.com/entry/sean-hannity-singapore-north-korea-summit_us_5b18484fe4b0734a993a92df',
 'https://www.huffingtonpost.com/entry/trump-obama-high-school-quote_us_5b14af82e4b010565aad1c77',
 'https://www.huffingtonpost.com/entry/food-stamp-work-requirements_us_5b047a15e4b07c4ea102c21c',
 'https://www.huffingtonpost.com/entry/ihop-name-change-ihob_us_5b17fd90e4b0599bc6df6c95',
 'https://www.huffingtonpost.com/entry/paul-kerr-democrats-california_us_5b12c1a9e4b0d5e89e200a8d',
 'https://www.huffingtonpost.com/entry/trump-asked-jeff-sessions-reverse-recusal-russia-probe-report_us_5b0de9dee4b0802d69cf5bf2',
 'https://www.huffingtonpost.com/entry/trump-amazon-larry-kudlow_us_5b01807fe4b0463cdba35548',
 'https://www.huffingtonpost.com/entry/parents-school-shooting-victims-call-out-moronic-gop-platitudes_us_5b019bf5e4b07309e059a218',
 'https://www.huffingtonpost.com/entry/texas-lt-governor-dan-patrick-doubles-down-on-arming-teachers_us_5b017c4be4b0463cdba350a5',
 'https://www.huffingtonpost.com/entry/scott-pruitt-pens_us_5b117b85e4b02143b7cc38a0',
 'https://www.huffingtonpost.com/entry/trump-jr-2016-help-gulf-princes-emissary_us_5b0080c9e4b0a046186c8156',
 'https://www.huffingtonpost.com/entry/trump-doj-justice-order_us_5b01b32ae4b0a046186d4305',
 'https://www.huffingtonpost.com/entry/mitt-romney-reveals-2016-vote-for-president_us_5b0fbd35e4b0fcd6a833c271',
 'https://www.huffingtonpost.com/entry/bill-de-blasio-smoking-marijuana-arrests_us_5b039e6ee4b0a046186f1b21',
 'https://www.huffingtonpost.com/entry/georgia-democrats-stacey-abrams-stacey-evans-new-american-majority_us_5b035fbee4b07309e05b787e',
 'https://www.huffingtonpost.com/entry/kentucky-democratic-primary-amy-mcgrath-fighter-pilot_us_5b042f57e4b0c0b8b23e79f8',
 'https://www.huffingtonpost.com/entry/retiring-lawmakers-campaign-funds_us_5afd6e19e4b0c1cf3c0c3eef',
 'https://www.huffingtonpost.com/entry/trump-giuliani-north-korea-mueller_us_5b06f625e4b05f0fc8460d6b',
 'https://www.huffingtonpost.com/entry/devin-nunes-wine-yacht-lawsuit_us_5b062622e4b0784cd2b12049',
 'https://www.huffingtonpost.com/entry/hugh-hewitt-trench-coats-guns_us_5b03a305e4b07309e05b8d4e',
 'https://www.huffingtonpost.com/entry/chinese-exclusion-act-immigration-politics_us_5b06a90fe4b05f0fc84552cf',
 'https://www.huffingtonpost.com/entry/ocasio-congress-candidate-new-york-crowley_us_5b11c598e4b0d5e89e1fbf2b',
 'https://www.huffingtonpost.com/entry/trump-says-hell-give-to-charity-for-royal-wedding-but-well-see_us_5afda6d2e4b0779345d6f748',
 'https://www.huffingtonpost.com/entry/trump-tariffs-corker-republican-senators_us_5b16bd54e4b09578259c2660',
 'https://www.huffingtonpost.com/entry/betsy-devos-now-says-she-doesnt-think-schools-can-call-ice-on-students_us_5b16b7e0e4b0734a9937e0cf',
 'https://www.huffingtonpost.com/entry/charles-kushner-calls-ethics-watchdogs-jerks_us_5b131622e4b010565aac756c',
 'https://www.huffingtonpost.com/entry/stormy-daniels-day-proclaimed_us_5b05adfbe4b0784cd2b0d414',
 'https://www.huffingtonpost.com/entry/white-house-sinkhole-twitter_us_5b04526ce4b0c0b8b23edcfe',
 'https://www.huffingtonpost.com/entry/california-schools-co-workers-red-flag-dangerous-gun-owners_us_5b044fdce4b003dc7e4700f7',
 'https://www.huffingtonpost.com/entry/courts-about-to-get-tougher-black-people_us_5b106d08e4b02143b7caf710',
 'https://www.huffingtonpost.com/entry/toddler-escapes-room_us_5b175395e4b0599bc6de1c0d',
 'https://www.huffingtonpost.com/entry/stacey-abrams-wins-democratic-nomination-for-governor_us_5b045d41e4b003dc7e471586',
 'https://www.huffingtonpost.com/entry/california-primary-election-results-democrats-dodge-lockouts_us_5b17d1c2e4b0734a9939817b',
 'https://www.huffingtonpost.com/entry/rudy-giuliani-jeff-sessions-russia-investigation-recusal_us_5b0ed3b9e4b0802d69d0a291',
 'https://www.huffingtonpost.com/entry/donald-trump-god-bless-america-lyrics_us_5b16f3f1e4b0599bc6ddec24',
 'https://www.huffingtonpost.com/entry/ohio-congressional-map-gerrymandering_us_5b056ee5e4b07c4ea103d092',
 'https://www.huffingtonpost.com/entry/rudy-giuliani-booed-yankees-stadium_us_5b0c5dade4b0fdb2aa55e279',
 'https://www.huffingtonpost.com/entry/doj-appeals-ruling-trump-twitter_us_5b164563e4b014707d27ddf4',
 'https://www.huffingtonpost.com/entry/immigrant-children-border-patrol-abuse_us_5b0685c7e4b07c4ea1051ef1',
 'https://www.huffingtonpost.com/entry/scandal-california-da-run-off-november_us_5b16ff33e4b09578259c9ff3',
 'https://www.huffingtonpost.com/entry/gabby-dimarco-foul-ball-beer-cup_us_5b1842bce4b0734a993a89bc',
 'https://www.huffingtonpost.com/entry/texas-school-shooting-gun-storage_us_5aff37e7e4b0a046186b87c8',
 'https://www.huffingtonpost.com/entry/donald-trumps-fight-with-nfl-players-national-anthem_us_5b16cbfae4b0599bc6dd9889',
 'https://www.huffingtonpost.com/entry/trump-giuliani-collusion_us_5b0487f8e4b05f0fc8429767',
 'https://www.huffingtonpost.com/entry/michael-cohen-threatens-reporter-tim-mak-over-rape-claim_us_5b107688e4b02143b7caf914',
 'https://www.huffingtonpost.com/entry/twitter-mocks-trump-summit-cancellation_us_5b06e058e4b07c4ea10612b2',
 'https://www.huffingtonpost.com/entry/americans-split-over-nfl-anthem-protest-ruling_us_5b0dc5ade4b0568a880f7e9b',
 'https://www.huffingtonpost.com/entry/alabama-sheriff-pocketed-food-money-loses-primary_us_5b175c8ee4b09578259cc5d9',
 'https://www.huffingtonpost.com/entry/fox-news-anchor-demolishes-trumps-tweet_us_5b0e179ae4b0fdb2aa57ce9d',
 'https://www.huffingtonpost.com/entry/puerto-rico-carmen-yul%C3%ADn-cruz-trump_us_5b103179e4b0fcd6a834da1c',
 'https://www.huffingtonpost.com/entry/alice-marie-johnson-trump-clemency_us_5b181768e4b09578259e59c7',
 'https://www.huffingtonpost.com/entry/j20-trial-trump-inauguration-felonies_us_5b16bf09e4b09578259c2baa',
 'https://www.huffingtonpost.com/entry/jared-kushner-security-clearance_us_5b05aec3e4b0784cd2b0d4a3',
 'https://www.huffingtonpost.com/entry/obama-photographer-donald-trump-animals_us_5afd2234e4b0779345d5dc5f',
 'https://www.huffingtonpost.com/entry/gop-rep-bill-apology-mccain_us_5afe8c74e4b07309e056a09d',
 'https://www.huffingtonpost.com/entry/chelsea-clinton-hypocrisy-samantha-bee-outrage_us_5b1059dae4b0d5e89e1e2a71',
 'https://www.huffingtonpost.com/entry/betsy-devos-uproar-schools-call-ice-undocumented-kids_us_5b05a297e4b05f0fc8441ce3',
 'https://www.huffingtonpost.com/entry/2018-midterms-democrats-avoided-disaster-but-that-might-not-be-enough_us_5b1802a5e4b09578259e29c8',
 'https://www.huffingtonpost.com/entry/john-boehner-no-republican-party_us_5b10de00e4b0d5e89e1e74cd',
 'https://www.huffingtonpost.com/entry/supreme-court-immigrant-teen-abortion_us_5b154ce5e4b02143b7ce9ec1',
 'https://www.huffingtonpost.com/entry/trump-letter-admits-he-dictated-misleading-statement-on-sons-meeting-with-russian_us_5b135a6ee4b0d5e89e2048dd',
 'https://www.huffingtonpost.com/entry/progressive-prosecutors-california-primary_us_5b0dc61de4b0568a880f7f3e',
 'https://www.huffingtonpost.com/entry/trumps-white-house-iftar-missing-american-muslim-groups_us_5b17eee1e4b09578259de352',
 'https://www.huffingtonpost.com/entry/trump-reacts-roseanne-canceled_us_5b0d93b1e4b0568a880f2b22',
 'https://www.huffingtonpost.com/entry/melania-trump-tweet-skeptical_us_5b0f0144e4b0dc84d07ffd27',
 'https://www.huffingtonpost.com/entry/scott-pruitt-epa-aides-scandal_us_5b155751e4b0d5e89e22018a',
 'https://www.huffingtonpost.com/entry/ice-deportation-separates-man-from-family_us_5b104987e4b0e096a4627497',
 'https://www.huffingtonpost.com/entry/ice-lgbtq-immigrant-detainees-sexual-assault_us_5b0daa5ce4b0fdb2aa5775a2',
 'https://www.huffingtonpost.com/entry/donald-trump-real-americans_us_5b017906e4b0463cdba34fa5',
 'https://www.huffingtonpost.com/entry/kushner-family-bailout-flagship-tower_us_5afddd50e4b06a3fb50eff6e',
 'https://www.huffingtonpost.com/entry/nunes-trump-russia-fundraising-doj_us_5afddaf7e4b06a3fb50efb5f',
 'https://www.huffingtonpost.com/entry/trump-hurricane-maria-puerto-rico-response_us_5b17ec5be4b0734a9939b2d5',
 'https://www.huffingtonpost.com/entry/google-maven-protests_us_5b119678e4b0d5e89e1fa730',
 'https://www.huffingtonpost.com/entry/pete-souza-shade-photo-book-trump_us_5b057903e4b07c4ea103e92b',
 'https://www.huffingtonpost.comhttp://www.huffingtonpost.com/topic/donald-trump',
 'https://www.huffingtonpost.com/entry/publix-suspends-contributions-to-nra-backed-politician-amid-protests_us_5b086551e4b0fdb2aa5387d7',
 'https://www.huffingtonpost.com/entry/wendy-rogers-arizona_us_5b05a67be4b07c4ea10457e2',
 'https://www.huffingtonpost.com/entry/richard-grenell-conservatives-europe_us_5b144fb4e4b010565aace78f',
 'https://www.huffingtonpost.com/entry/right-wing-millennial-machine_us_5b049aebe4b07c4ea102e0c3',
 'https://www.huffingtonpost.com/entry/new-mexico-democrats_us_5b0d7e65e4b0802d69ced56f',
 'https://www.huffingtonpost.com/entry/court-ruling-currency-in-god-we-trust_us_5b1559d3e4b02143b7cec52f',
 'https://www.huffingtonpost.com/entry/trump-giuliani-cohen-money_us_5afde92be4b0779345d75920',
 'https://www.huffingtonpost.com/entry/nra-santa-fe-school-shooting_us_5b05c2eae4b07c4ea104731e',
 'https://www.huffingtonpost.com/entry/blake-farenthold-lobbyist-job-sexual-harassment_us_5b02f6bae4b07309e05af5e6',
 'https://www.huffingtonpost.com/entry/border-agent-fatally-shoots-migrant-woman-in-texas_us_5b0706a1e4b0784cd2b2d714',
 'https://www.huffingtonpost.com/entry/mark-kelly-slams-donothing-trump-on-guns_us_5affb07ce4b0463cdba1f27c',
 'https://www.huffingtonpost.com/entry/ted-cruz-santa-fe-shooting-tweet_us_5aff5183e4b07309e058098a',
 'https://www.huffingtonpost.com/entry/anthony-perkins-tab-hunter-movie-jj-abrams-zachary-quinto_us_5b186148e4b0599bc6e023f0',
 'https://www.huffingtonpost.com/entry/giuliani-trump-cuomo-obstruction-charge-interview_us_5afed6aee4b07309e0575c3d',
 'https://www.huffingtonpost.com/entry/donald-trump-jay-z_us_5b0e06a9e4b0802d69cf66fc',
 'https://www.huffingtonpost.com/entry/patti-davis-ronald-reagan-donald-trump_us_5b150127e4b02143b7cddf38',
 'https://www.huffingtonpost.com/entry/jim-carrey-nfl-donald-trump_us_5b0e7ea1e4b0fdb2aa585afe',
 'https://www.huffingtonpost.com/entry/civil-rights-groups-senate-bill-sexual-harassment-policy_us_5b0714e3e4b07c4ea1066816',
 'https://www.huffingtonpost.com/entry/edward-snowden-trump-loves-putin_us_5b08ae41e4b0568a880b7451',
 'https://www.huffingtonpost.com/entry/missouri-governor-eric-greitens-resigns_us_5acedd7be4b0701783ab520e',
 'https://www.huffingtonpost.com/entry/federal-prosecutors-trump-inauguration-protesters-felons_us_5afc6383e4b0779345d52bb3',
 'https://www.huffingtonpost.com/entry/oceans-8-cast-red-carpet_us_5b16ba63e4b09578259c1b01',
 'https://www.huffingtonpost.com/entry/california-democrat-gavin-newsom-attacks-john-cox_us_5b12ca41e4b02143b7cccbd7',
 'https://www.huffingtonpost.comhttps://www.huffingtonpost.com/topic/gun-control',
 'https://www.huffingtonpost.com/entry/refugee-office-that-lost-1500-kids-not-legally-responsible-for-finding-them_us_5b09954ee4b0802d69cbc52e',
 'https://www.huffingtonpost.com/entry/democrats-not-invited-fbi-informant_us_5b052ddce4b07c4ea10350c4',
 'https://www.huffingtonpost.com/entry/farm-bill-animals-king-amendment_us_5afb4840e4b0779345d3cb4a',
 'https://www.huffingtonpost.com/entry/trump-new-domestic-gag-rule-planned-parenthood_us_5afef8cce4b0a046186b2e39',
 'https://www.huffingtonpost.com/entry/trump-russia-mueller-fox-news_us_5aff072de4b0a046186b4794',
 'https://www.huffingtonpost.com/entry/trump-phone-security_us_5b03ca69e4b0463cdba5774c',
 'https://www.huffingtonpost.com/entry/native-american-woman-congress_us_5b16ffbfe4b0599bc6ddfa24',
 'https://www.huffingtonpost.com/entry/bill-gates-trump-difference-hpv-hiv_us_5afe0bfbe4b07309e0564cdf',
 'https://www.huffingtonpost.com/entry/twitter-bots-may-have-delivered-donald-trumps-victory-research-finds_us_5b07a231e4b0568a8809c66a',
 'https://www.huffingtonpost.com/entry/trump-shoot-comey_us_5b145897e4b02143b7cd633e',
 'https://www.huffingtonpost.com/entry/jeff-flake-spygate-trump-mueller_us_5b0af69de4b0802d69cc5c7b',
 'https://www.huffingtonpost.com/entry/white-house-ignore-climate-research-report_us_5b066bf7e4b07c4ea104e2a7',
 'https://www.huffingtonpost.com/entry/bill-clinton-monica-lewinsky_us_5b1521f4e4b010565aadaddc',
 'https://www.huffingtonpost.com/entry/ex-trump-adviser-informant-embarrassing_us_5b03fed4e4b07309e05c2058',
 'https://www.huffingtonpost.com/entry/trump-responds-santa-fe-shooting-prison-reform_us_5afeef6de4b07309e0578ae8',
 'https://www.huffingtonpost.com/entry/cate-blanchett-and-sara-paulson-absolutely-lose-it-during-live-interview_us_5b17db8de4b0599bc6df1bb9',
 'https://www.huffingtonpost.com/entry/michael-mcallister-alabama-governor_us_5b17560be4b0734a9938942a',
 'https://www.huffingtonpost.com/entry/cindy-axne-abby-finkenauer_us_5b175bdce4b0599bc6de1e86',
 'https://www.huffingtonpost.com/entry/pruitt-vip-sports-seats-from-coal-baron_us_5b137c6ee4b0d5e89e204e90',
 'https://www.huffingtonpost.com/entry/trump-lies-media_us_5b1849fee4b0599bc6e01bf1',
 'https://www.huffingtonpost.com/entry/conservative-jeff-van-drew-wins-democratic-primary_us_5b175804e4b09578259cc45f',
 'https://www.huffingtonpost.com/entry/forced-arbitration-sexual-harassment_us_5afda846e4b0a59b4e019e0a',
 'https://www.huffingtonpost.com/entry/giuliani-russia-probe-legal-battle_us_5b136446e4b010565aac92c8',
 'https://www.huffingtonpost.com/entry/greg-abbott-texas-shotgun_us_5b01a23ee4b0463cdba37d6c',
 'https://www.huffingtonpost.com/entry/border-patrol-shooting-shakes-town-where-illegal-crossings-are-part-of-daily-life_us_5b102e37e4b0fcd6a834d106',
 'https://www.huffingtonpost.com/entry/dnc-members-angry-with-tom-perez-for-endorsing-andrew-cuomo_us_5b0ddf12e4b0568a880f8d48',
 'https://www.huffingtonpost.com/entry/george-papadopoulos-trump-pardon-simona-mangiante_us_5b161bb8e4b093ac33a125d3',
 'https://www.huffingtonpost.com/entry/students-sit-in-gun-control-paul-ryan-arrested_us_5aff456ae4b0463cdba1dd29',
 'https://www.huffingtonpost.com/entry/trump-inauguration-trial-j20_us_5b155d5be4b010565aae50d4',
 'https://www.huffingtonpost.com/entry/liberal-billionaire-tom-steyer-millennials-impeachment_us_5afef4b2e4b07309e05793fd',
 'https://www.huffingtonpost.com/entry/cynthia-nixon-keep-fighting-governor-andrew-cuomo_us_5b067660e4b07c4ea104f93d',
 'https://www.huffingtonpost.com/entry/manafort-tamper-witnesses_us_5b15de77e4b0129b529d3da9',
 'https://www.huffingtonpost.com/entry/trump-calls-own-official-a-nonexistent-new-york-times-source_us_5b09e95de4b0fdb2aa54344a',
 'https://www.huffingtonpost.com/entry/trump-right-pardon-himself_us_5b15336ee4b010565aadd774',
 'https://www.huffingtonpost.com/entry/whistleblower-michael-cohen-suspicious-activity-reports_us_5afcd865e4b0779345d5b933',
 'https://www.huffingtonpost.com/entry/doj-meeting-trump-fbi_us_5b06e0f4e4b07c4ea10613b3',
 'https://www.huffingtonpost.com/entry/college-graduates-trump-era_us_5b103ac3e4b0400b2330a69a',
 'https://www.huffingtonpost.com/entry/michelle-wolf-says-sarah-huckabee-sanders-has-the-mario-batali-of-personalities_us_5b0c2548e4b0568a880d94f7',
 'https://www.huffingtonpost.com/entry/hayden-accuses-trump-of-doing-anything-to-hurt-mueller-proble_us_5b0b476fe4b0802d69cc6a14',
 'https://www.huffingtonpost.com/entry/adia-mclellan-winfrey-alabama-congress-democrat_us_5b15e09be4b093ac33a10afb',
 'https://www.huffingtonpost.com/entry/iraq-parliament-christians-badr-organization_us_5b05dfd0e4b07c4ea104961f',
 'https://www.huffingtonpost.com/entry/trump-nasa-jim-bridenstine-climate-change_us_5afe9b49e4b0a046186a4f3b',
 'https://www.huffingtonpost.com/entry/nfl-philadelphia-eagles-players-hit-back-at-trumps-disinvitation_us_5b168510e4b014707d28638d',
 'https://www.huffingtonpost.com/entry/kim-kardashian-donald-trump-prison-reform-meeting-twitter_us_5b0f3565e4b05ef4c22a8349',
 'https://www.huffingtonpost.com/entry/facebook-ad-disclosure_us_5b070d61e4b05f0fc8463453',
 'https://www.huffingtonpost.com/entry/roger-stone-damaging-clinton-emails-wikileaks_us_5b073dc7e4b0802d69c979d7',
 'https://www.huffingtonpost.com/entry/lizzie-fletcher-wins-democratic-primary-texas-7th-houston-laura-moser_us_5b049815e4b0784cd2af5303',
 'https://www.huffingtonpost.com/entry/does-rush-limbaugh-matter-anymore_us_5b0d8f64e4b0568a880f23cd',
 'https://www.huffingtonpost.com/entry/chelsea-clinton-trump-degreades_us_5b0a9e10e4b0fdb2aa547d4e',
 'https://www.huffingtonpost.com/entry/fair-just-prosecution-criminal-justice-reform_us_5aff5a94e4b0463cdba1e59d',
 'https://www.huffingtonpost.com/entry/imagine-dragons-dan-reynolds-ellen-degeneres_us_5b1742b4e4b09578259cc01a',
 'https://www.huffingtonpost.com/entry/keith-ellison-running-for-minnesota-attorney-general_us_5b15b5c3e4b014707d2768d1',
 'https://www.huffingtonpost.com/entry/republicans-are-picking-who-will-take-on-a-top-trump-target-in-montana_us_5b1555a1e4b02143b7ceb936',
 'https://www.huffingtonpost.com/entry/obama-photog-pete-souza-trolls-trump-spy-claim_us_5b08f77ee4b0568a880b8752',
 'https://www.huffingtonpost.com/entry/publix-boycott-putnam-donations_us_5b040d5ce4b0463cdba5febe',
 'https://www.huffingtonpost.com/entry/california-primaries-glorious-mess-congress_us_5b144bf4e4b02143b7cd5b65',
 'https://www.huffingtonpost.com/entry/rhode-island-gun-laws_us_5b1147c3e4b02143b7cbc234',
 'https://www.huffingtonpost.com/entry/jennifer-lawrence-reportedly-dating-non-famous-person_us_5b18228ae4b09578259e70df',
 'https://www.huffingtonpost.com/entry/jack-johnson-taboo-sex-criminalized_us_5b08718be4b0802d69cb376a',
 'https://www.huffingtonpost.com/entry/richard-painter-minnesota-senate_us_5b0eeb2be4b0802d69d0d6c1',
 'https://www.huffingtonpost.com/entry/gina-haspel-torture-confirmed_us_5afdb75fe4b0a59b4e01c1a5',
 'https://www.huffingtonpost.com/entry/report-michael-cohens-business-partner-cooperating-with-prosecutors_us_5b04e335e4b07c4ea10304a1',
 'https://www.huffingtonpost.comhttps://www.huffingtonpost.com/topic/nra',
 'https://www.huffingtonpost.com/entry/eagles-white-house-super-bowl-event_us_5b16b57de4b09578259c06a0',
 'https://www.huffingtonpost.com/entry/scott-pruitt-scandals_us_5b16ef35e4b0734a99385b09',
 'https://www.huffingtonpost.com/entry/melania-trump-first-public-appearance_us_5b16ba0be4b09578259c1931',
 'https://www.huffingtonpost.com/entry/scott-pruitt-used-trump-mattress_us_5b156404e4b02143b7cedbd4',
 'https://www.huffingtonpost.com/entry/george-hw-bush-hospitalized_us_5b0af673e4b0fdb2aa54b625',
 'https://www.huffingtonpost.com/entry/supreme-courts-ruling-this-week-is-already-screwing-thousands-of-chipotle-workers_us_5b0844aae4b0568a880b3e26',
 'https://www.huffingtonpost.com/entry/china-tariffs_us_5b0d4754e4b0fdb2aa56d543',
 'https://www.huffingtonpost.com/entry/agent-orange-may-be-responsible-for-more-veteran-deaths-than-the-government-is-willing-to-recognize_us_5b05b4f1e4b07c4ea1046787',
 'https://www.huffingtonpost.com/entry/trump-democrats-myanmar-rohingya_us_5afda19be4b0a59b4e01907d',
 'https://www.huffingtonpost.com/entry/irelands-historic-abortion-vote-haunted-trump-brexit_us_5b06d25ae4b05f0fc845b572',
 'https://www.huffingtonpost.com/entry/sarah-huckabee-sanders-slams-samantha-bee-for-ivanka-comments-implores-tbs-to-act_us_5b10283de4b0870ebd097b35',
 'https://www.huffingtonpost.com/entry/democrats-school-funding-teacher-walkouts_us_5b043ff3e4b0740c25e5c2d8',
 'https://www.huffingtonpost.com/entry/virginia-senate-medicaid-expansion-promising-health-coverage-to-almost-400000_us_5b0d94dde4b0802d69cef7ce',
 'https://www.huffingtonpost.com/entry/judge-temporarily-bans-iowa-abortion-law_us_5b116b26e4b0d5e89e1f55e2',
 'https://www.huffingtonpost.com/entry/women-won-primary-elections_us_5b17dacee4b09578259dc595',
 'https://www.huffingtonpost.com/entry/texas-democrat-laura-moser-joins-strong-arm-press_us_5b182a7fe4b09578259e884e',
 'https://www.huffingtonpost.com/entry/zach-wahls-iowa-state-senate-primary-democrat-lesbian-moms-viral_us_5b17698fe4b09578259cca92',
 'https://www.huffingtonpost.com/entry/vietnam-test-united-states-abandons-climate-diplomacy_us_5b030f8fe4b0a046186eab04',
 'https://www.huffingtonpost.com/entry/arnold-schwarzenegger-donald-trump-tweet_us_5b11798ae4b02143b7cc3361',
 'https://www.huffingtonpost.com/entry/michigan-medicaid-work-requirement-racist-policy_us_5b0d657be4b0802d69cea93c',
 'https://www.huffingtonpost.com/entry/hillary-clinton-trump-russian-hat_us_5b0275ffe4b07309e05a02c9',
 'https://www.huffingtonpost.com/entry/supreme-court-masterpiece-cake-shop_us_5b1549ece4b02143b7ce938a',
 'https://www.huffingtonpost.com/entry/mitch-mcconnell-tony-perkins-religious-freedom_us_5afdd6bee4b0a59b4e01e1ab',
 'https://www.huffingtonpost.com/entry/giuliani-trump-probably-does-have-power-pardon-himself-but-wont_us_5b13e859e4b010565aacbc6b',
 'https://www.huffingtonpost.com/entry/carmen-yulin-cruz-slams-trumps-human-rights-violations-in-puerto-rico_us_5b14b64fe4b02143b7cd9421',
 'https://www.huffingtonpost.com/entry/sarah-sanders-child-reporter-school-shootings_us_5b0ef9a4e4b0dc84d07ff011',
 'https://www.huffingtonpost.com/entry/north-korea-still-committed-to-trump-meeting_us_5b0a0b0be4b0568a880c0a60',
 'https://www.huffingtonpost.com/entry/gop-congressman-abandons-re-election-alcoholism-thomas-garrett_us_5b0c8f24e4b0fdb2aa55f781',
 'https://www.huffingtonpost.com/entry/betsy-devos-school-shootings_us_5b16c97ce4b09578259c3ac6',
 'https://www.huffingtonpost.com/entry/progressive-prosecutors-california-primaries_us_5b117d36e4b010565aabc778',
 'https://www.huffingtonpost.com/entry/stormy-daniels-old-attorney-trump-puppet_us_5b182a10e4b09578259e87af',
 'https://www.huffingtonpost.com/entry/nathan-larson-congressional-candidate-pedophile_us_5b10916de4b0d5e89e1e4824',
 'https://www.huffingtonpost.com/entry/results-for-irelands-historic-abortion-referendum-show-yes-vote-leads_us_5b086497e4b0802d69cb2cff',
 'https://www.huffingtonpost.com/entry/scam-pac-arrest_us_5afdea34e4b0a59b4e01ffa8',
 'https://www.huffingtonpost.com/entry/texas-guns-school-safety-plan_us_5b0ed45ae4b0568a8810d7bd',
 'https://www.huffingtonpost.com/entry/san-francisco-ban-flavored-tobacco_us_5b171f51e4b0599bc6de0fd0',
 'https://www.huffingtonpost.com/entry/lawyer-anti-spanish-eviction-complaint_us_5afe01efe4b0a0461869d54d',
 'https://www.huffingtonpost.com/entry/donald-trump-laurel-yanny-debate-video_us_5afe73dee4b0a046186a0d1d',
 'https://www.huffingtonpost.com/entry/jason-alexander-rohrabacher-dino-fart-ad_us_5b10a106e4b02143b7cb0d47',
 'https://www.huffingtonpost.com/entry/chris-cillizza-posts-numbers_us_5b0eedbde4b0802d69d0db73',
 'https://www.huffingtonpost.com/entry/trump-inauguration-trial-j20_us_5b0f19a3e4b05ef4c22a76d3',
 'https://www.huffingtonpost.com/entry/carl-bernstein-donald-trump-authoritarianism_us_5b0bf74ae4b0568a880d4d76',
 'https://www.huffingtonpost.com/entry/david-spade-kate-spade-death_us_5b17ac85e4b09578259d4139',
 'https://www.huffingtonpost.com/entry/meek-mill-backs-out-trump-event-prison-refor_us_5afef2a5e4b0463cdba168d6',
 'https://www.huffingtonpost.com/entry/melania-skipping-g7-and-singapore_us_5b146f04e4b02143b7cd711e',
 'https://www.huffingtonpost.com/entry/obamacare-premiums-will-be-way-higher-next-year-they-didnt-have-to-be_us_5afdf024e4b07309e056334e',
 'https://www.huffingtonpost.com/entry/interior-department-thumbed-nose-probe-zinke_us_5afdfc4ce4b0463cdba0133e',
 'https://www.huffingtonpost.com/entry/poll-abc-cancel-roseanne_us_5b106040e4b0d5e89e1e2f76',
 'https://www.huffingtonpost.com/entry/ivanka-cuddle-pic-missing-migrant-kids_us_5b0b34afe4b0fdb2aa54c215',
 'https://www.huffingtonpost.com/entry/scott-pruitt-epa-chick-fil-a_us_5b1833cfe4b0599bc6dfeeb1',
 'https://www.huffingtonpost.com/entry/howard-stern-donald-trump-ivanka-david-letterman_us_5b02fc36e4b07309e05aff01',
 'https://www.huffingtonpost.com/entry/dinesh-dsouza-convicted-felon-pardoned-by-trump-has-done-some-vile-things_us_5b1007efe4b05ef4c22bbf94',
 'https://www.huffingtonpost.com/entry/trump-meeting-santa-fe-shooting-victims_us_5b114e84e4b0d5e89e1f139a',
 'https://www.huffingtonpost.com/entry/gina-ortiz-jones-congress-texas_us_5b043424e4b003dc7e46b984',
 'https://www.huffingtonpost.com/entry/polling-choice-obscure-neo-nazi-senate-contender-california_us_5b16e9b9e4b0599bc6ddd73d',
 'https://www.huffingtonpost.com/entry/boulder-colorado-assault-weapon-ban_us_5afd4356e4b0779345d61ec1',
 'https://www.huffingtonpost.com/entry/diane-black-porn-school-gun-violence_us_5b0d6634e4b0568a880ede65',
 'https://www.huffingtonpost.com/entry/chelsea-clinton-twitter-troll_us_5b10c4c3e4b010565aaaab85',
 'https://www.huffingtonpost.com/entry/trump-kim-summit-back-on-north-korea_us_5b0f5d44e4b0fcd6a8334a2a',
 'https://www.huffingtonpost.com/entry/equal-rights-amendment-illinois_us_5b0f9599e4b05ef4c22ac411',
 'https://www.huffingtonpost.com/entry/jeff-sessions-uses-exceptional-power-immigration_us_5afe321be4b0a0461869e928',
 'https://www.huffingtonpost.com/entry/indiana-teacher-transgender-school-policy_us_5b17f162e4b0599bc6df3caf',
 'https://www.huffingtonpost.com/entry/north-korea-official-headed-to-us_us_5b0d30e1e4b0568a880e821f',
 'https://www.huffingtonpost.com/entry/trump-kim-summit-winner_us_5b11ac04e4b0d5e89e1fb60c',
 'https://www.huffingtonpost.com/entry/montana-auditor-will-face-trump-target-tester-in-november_us_5b15ac9be4b093ac33a0ecf9',
 'https://www.huffingtonpost.com/entry/rudy-giuliani-boos-love-yankee-stadium_us_5b0fae91e4b0870ebd085170',
 'https://www.huffingtonpost.com/entry/we-asked-the-american-public-to-settle-five-of-the-internets-dumbest-controversies_us_5afdf4eae4b07309e05637f0',
 'https://www.huffingtonpost.com/entry/santa-fe-shooting-gun-violence-protest_us_5aff0885e4b07309e057b83e',
 'https://www.huffingtonpost.com/entry/jeff-merkley-immigration-detention-center_us_5b149d32e4b010565aad1076',
 'https://www.huffingtonpost.com/entry/gop-lawmakers-classified-info-fbi-informant_us_5b03cb68e4b0463cdba5786e']
more_articles = list(set(more_articles))


#Same as above but for expanded list, phase 1
more_list_o_articles = []
more_problem_articles = []
for text in more_articles:
    #print(text)
    try:
        art = get_parsed_article_from_link(text.encode())
        more_list_o_articles.append(art)

    except:
        print("Problem processing url " + text)
        problem = text
        more_problem_articles.append(problem)
    time.sleep(2)
driver = driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
#same as above for expanded list, phase 2
for x in more_problem_articles:
    try:
        driver.get(x)
        time.sleep(3)
        soupy = BeautifulSoup(driver.page_source, 'lxml')
        title = soupy.find('h1', class_='headline__title').text
        body = soupy.find('div', class_='entry__text js-entry-text yr-entry-text').text

        articley = {
            'title': title,
            'body': body,
            'source': 'Huffington Post',
            'num_source': 1
        }

        more_list_o_articles.append(articley)
    except:
        pass
#starts client in Mongodb
client = MongoClient()
biased_news = client.project5.biased_news
#creates event and loads articles into Mongodb
db = client.events
biased_news = db.biased_news
biased_news.insert_many(more_list_o_articles)
