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
mj_first_articles = (
['https://www.motherjones.com/politics/2018/06/mueller-schiff-perjury/',
'https://www.motherjones.com/politics/2018/06/jeff-sessions-who-marijuana-review/',
'https://www.motherjones.com/politics/2018/06/trump-comey-firing-where-is-my-thank-you/',
'https://www.motherjones.com/politics/2018/06/canada-set-legalize-recreational-marijuana-cannabis-united-states/',
'https://www.motherjones.com/politics/2018/06/heres-what-massachusetts-moderate-gop-governor-has-in-common-with-trump/',
'https://www.motherjones.com/politics/2018/06/republicans-want-to-use-the-census-to-radically-change-political-representation/',
'https://www.motherjones.com/politics/2018/06/trump-loyalty-republican-primaries/',
'https://www.motherjones.com/politics/2018/06/this-evangelical-pastor-helped-build-the-religious-right-he-now-believes-he-made-a-terrible-mistake-rob-schenck/',
'https://www.motherjones.com/politics/2018/06/trump-manafort-mistakes-david-corn-russia-podcast/',
'https://www.motherjones.com/politics/2018/06/federal-judge-strikes-blow-against-trump-administration-separation-of-families-border-1/',
'https://www.motherjones.com/politics/2018/06/north-carolina-republicans-want-a-constitutional-amendment-to-require-id-to-vote/',
'https://www.motherjones.com/politics/2018/06/did-the-supreme-court-fall-for-a-stunt/',
'https://www.motherjones.com/politics/2018/06/cfpb-advisory-boards-fired/',
'https://www.motherjones.com/politics/2018/06/rudy-giuliani-stormy-daniels-porn-feminist/',
'https://www.motherjones.com/politics/2018/06/jeanine-pirro-wants-to-be-attorney-general-first-she-has-to-get-jeff-sessions-fired/',
'https://www.motherjones.com/politics/2018/06/melania-trump-rudy-giuliani-stormy-daniels-donald-trump/',
'https://www.motherjones.com/politics/2018/06/more-democrats-running-than-republicans-texas/',
'https://www.motherjones.com/politics/2018/06/sean-patrick-maloney-new-york-attorney-general-democrats-congress/',
'https://www.motherjones.com/politics/2018/06/40-democratic-senators-call-on-trump-to-end-family-separations-at-the-border/'])

mj_more_articles = (
['https://www.motherjones.com/politics/2018/04/trumps-tweet-about-stormy-daniels-backfired-and-now-shes-suing-for-defamation/',
'https://www.motherjones.com/politics/2018/04/democrats-recruited-two-sandy-hook-parents-to-run-for-congress-they-both-decided-it-wasnt-worth-it/',
'https://www.motherjones.com/politics/2018/04/trump-is-undermining-his-own-immigration-agenda-with-attacks-on-mexico/',
'https://www.motherjones.com/politics/2018/04/trump-began-his-morning-by-attacking-a-times-reporter-on-twitter/',
'https://www.motherjones.com/politics/2018/04/trump-comey-tweet-committed-many-crimes-clinton/',
'https://www.motherjones.com/politics/2018/04/house-republicans-just-ramped-up-their-investigation-of-epa-administrator-scott-pruitt/',
'https://www.motherjones.com/politics/2018/05/after-violent-may-day-protests-a-federal-judge-orders-an-investigation-into-puerto-rican-police/',
'https://www.motherjones.com/politics/2018/03/cambridge-analytica-ford-coca-cola-trump/',
'https://www.motherjones.com/politics/2018/05/paige-curry-santa-fe-high-school-shooting-interview/',
'https://www.motherjones.com/politics/2018/05/facebook-is-enlisting-these-disinformation-detection-pros-to-fight-fake-news/',
'https://www.motherjones.com/politics/2018/05/new-ad-targets-devin-nunes/',
'https://www.motherjones.com/politics/2018/04/top-republican-official-says-trump-won-wisconsin-because-of-voter-id-law/',
'https://www.motherjones.com/politics/2018/04/james-comey-just-responded-to-donald-trumps-attacks/',
'https://www.motherjones.com/politics/2018/04/enjoy-this-excruciating-clip-of-trump-brushing-off-dandruff-from-macrons-suit/',
'https://www.motherjones.com/politics/2018/05/no-one-had-seen-these-tiny-deer-for-20-years-then-one-day-they-came-back/',
'https://www.motherjones.com/politics/2018/04/ronny-jackson-withdraws-nomination-for-veterans-affairs-secretary/',
'https://www.motherjones.com/politics/2018/05/trump-administration-could-send-57000-hondurans-to-one-of-the-worlds-most-dangerous-places/',
'https://www.motherjones.com/politics/2018/06/harley-rouda-314-action-attack-ad/',
'https://www.motherjones.com/politics/2018/03/devin-nunes-is-raising-money-off-his-shoddy-trump-russia-investigation/',
'https://www.motherjones.com/politics/2018/05/trump-blames-the-democrats-for-family-separation-at-the-mexican-border/',
'https://www.motherjones.com/politics/2018/05/the-bbc-just-trolled-donald-trump-and-it-was-epic/',
'https://www.motherjones.com/politics/2018/04/sessions-turned-to-a-convicted-republican-fundraiser-for-advice-on-lining-up-new-u-s-attorneys/',
'https://www.motherjones.com/politics/2018/04/speaker-paul-ryan-to-retire-from-congress/',
'https://www.motherjones.com/politics/2018/03/andrew-mccabes-gofundme-just-broke-500000/',
'https://www.motherjones.com/politics/2018/04/the-trump-administration-just-announced-more-sanctions-against-russia/',
'https://www.motherjones.com/politics/2018/04/how-one-high-school-teacher-learned-to-take-teenagers-seriously/',
'https://www.motherjones.com/politics/2018/04/special-counsel-robert-mueller-is-asking-russian-oligarchs-if-they-gave-money-to-trump/',
'https://www.motherjones.com/politics/2018/04/trump-announces-hes-considering-interfering-with-justice-department-investigations/',
'https://www.motherjones.com/politics/2018/06/new-york-times-secret-legal-letter-trump/',
'https://www.motherjones.com/politics/2018/04/michelle-wolfs-scathing-comedy-set-at-the-whcd-provoked-outrage-glee-and-everything-in-between/',
'https://www.motherjones.com/politics/2018/04/the-parkland-effect-might-cost-this-republican-her-seat-in-congress/',
'https://www.motherjones.com/politics/2018/05/morning-joe-mika-brzezinski-trump-surgeon-mar-a-lago/',
'https://www.motherjones.com/politics/2018/04/mike-pompeo-says-he-wouldnt-resign-over-muellers-firing/',
'https://www.motherjones.com/politics/2018/05/michael-cohen-just-mortgaged-his-prized-trump-condo/',
'https://www.motherjones.com/politics/2018/06/hundreds-of-children-are-being-held-at-the-border-for-longer-than-the-law-typically-allows/',
'https://www.motherjones.com/politics/2018/05/the-firm-that-paid-michael-cohen-500000-is-deeply-tied-to-a-russian-oligarch-records-show/',
'https://www.motherjones.com/politics/2018/03/it-took-3-different-court-orders-for-scott-walker-to-finally-hold-constitutionally-required-elections/',
'https://www.motherjones.com/politics/2018/05/these-evangelicals-are-turning-ar-15s-into-garden-hoes/',
'https://www.motherjones.com/politics/2018/05/trump-slams-the-nyt-for-reporting-what-a-white-house-official-told-them/',
'https://www.motherjones.com/politics/2018/04/michael-cohen-abandons-lawsuits-he-filed-arguing-the-steel-dossier-is-false/',
'https://www.motherjones.com/politics/2018/04/trump-is-considering-another-presidential-pardon/',
'https://www.motherjones.com/politics/2018/04/trump-wont-impose-the-russia-sanctions-his-administration-announced-yesterday/',
'https://www.motherjones.com/politics/2018/04/michael-cohen-once-the-presidents-trusted-fixer-emerges-as-his-greatest-liability/',
'https://www.motherjones.com/politics/2018/05/iowa-lawmakers-just-passed-a-bill-to-ban-abortion-after-six-weeks/',
'https://www.motherjones.com/politics/2018/05/north-carolina-teachers-are-taking-to-the-streets-heres-what-theyre-demanding/',
'https://www.motherjones.com/politics/2018/05/rudy-giuliani-tv-interviews-greenberg-traurig-trump/',
'https://www.motherjones.com/politics/2018/04/the-head-of-the-deutsche-bank-division-that-loaned-trump-364-million-just-got-a-big-promotion/',
'https://www.motherjones.com/politics/2018/04/teachers-have-been-getting-screwed-in-oklahoma-for-generations/',
'https://www.motherjones.com/politics/2018/04/trump-and-trolls-target-caravan-of-migrant-families/',
'https://www.motherjones.com/politics/2018/04/what-the-heck-happened-in-gaza-this-weekend/',
'https://www.motherjones.com/politics/2018/05/mike-braun-just-won-indianas-insane-republican-senate-primary/',
'https://www.motherjones.com/politics/2018/04/donald-trump-really-wants-you-to-know-how-well-hes-doing-in-one-specific-poll/',
'https://www.motherjones.com/politics/2018/05/the-new-york-times-just-revealed-a-second-trump-tower-meeting/',
'https://www.motherjones.com/politics/2018/05/the-pentagon-considers-this-russian-sniper-rifle-a-big-threat-to-us-soldiers-the-nra-helped-promote-it/',
'https://www.motherjones.com/politics/2018/04/get-going-before-youre-ready-outgoing-planned-parenthood-head-cecile-richards-has-advice-for-new-activists/',
'https://www.motherjones.com/politics/2018/04/waffle-house-travis-reinking-weapons/',
'https://www.motherjones.com/politics/2018/06/aclu-sues-trump-over-census-a-naked-act-of-intentional-discrimination/',
'https://www.motherjones.com/politics/2018/04/why-the-scooter-libby-case-and-trumps-pardon-really-really-matter/',
'https://www.motherjones.com/politics/2018/06/brock-turner-judge-persky-recall-election/',
'https://www.motherjones.com/politics/2018/04/bill-cosby-was-just-found-guilty-of-sexual-assault/',
'https://www.motherjones.com/politics/2018/04/kentuckys-gop-governor-says-teacher-protests-enable-child-sexual-assault/',
'https://www.motherjones.com/politics/2018/06/keith-ellison-minnesota-attorney-general-dnc-congress/',
'https://www.motherjones.com/politics/2018/05/at-least-8-dead-in-santa-fe-high-school-shooting/',
'https://www.motherjones.com/politics/2018/05/rudy-giuliani-definitely-did-not-make-things-better-for-trump-in-this-abc-interview/',
'https://www.motherjones.com/politics/2018/03/the-supreme-court-cant-figure-out-how-to-fix-partisan-gerrymandering/',
'https://www.motherjones.com/politics/2018/04/a-republican-congressman-met-with-constituents-pulled-out-a-loaded-gun-and-then-said-he-wouldnt-be-a-gabby-giffords/',
'https://www.motherjones.com/politics/2018/03/trumps-plan-to-rig-the-census-explained/',
'https://www.motherjones.com/politics/2018/05/heres-how-the-government-managed-to-lose-track-of-1500-migrant-children/',
'https://www.motherjones.com/politics/2018/05/grover-norquist-has-lost-his-spot-in-the-nras-inner-circle/',
'https://www.motherjones.com/politics/2018/04/barbara-bush-dies-at-92/',
'https://www.motherjones.com/politics/2018/05/emerdata-cambridge-analytica-shutting-down-facebook-trump/',
'https://www.motherjones.com/politics/2018/05/missouri-might-impeach-its-governor-amid-sexual-assault-allegations/',
'https://www.motherjones.com/politics/2018/04/pruitt-epa-whistleblower-private-jet-hotel/',
'https://www.motherjones.com/politics/2018/04/new-data-shows-how-trump-is-targeting-immigrants-who-have-been-here-for-years/',
'https://www.motherjones.com/politics/2018/05/nra-leader-once-worked-for-professor-who-claimed-blacks-were-genetically-inferior/',
'https://www.motherjones.com/politics/2018/06/trump-puerto-rico-hurricane-maria-still-bragging/',
'https://www.motherjones.com/politics/2018/04/texas-democrats-just-got-a-huge-boost-thanks-to-this-court-decision/',
'https://www.motherjones.com/politics/2018/04/this-is-what-mark-zuckerberg-will-tell-congress-about-facebooks-privacy-crisis/',
'https://www.motherjones.com/politics/2018/04/a-new-trump-administration-proposal-could-triple-low-income-families-rent/',
'https://www.motherjones.com/politics/2018/05/rudy-giuliani-trumps-lawyer-is-spending-memorial-day-weekend-raving-about-how-the-mueller-investigation-is-rigged/',
'https://www.motherjones.com/politics/2018/06/dana-rohrabacher-russia-california-election-primary/',
'https://www.motherjones.com/politics/2018/05/todays-high-school-massacre-is-texass-8th-mass-shooting-since-1984/',
'https://www.motherjones.com/politics/2018/04/new-report-details-dozens-of-corrupt-border-patrol-agents-just-as-trump-wants-to-hire-more/',
'https://www.motherjones.com/politics/2018/05/rudy-giuliani-says-trump-paid-stormy-daniels/',
'https://www.motherjones.com/politics/2018/04/read-the-transcript-of-james-comeys-interview-about-donald-trump/',
'https://www.motherjones.com/politics/2018/05/robert-mueller-donald-trump-michael-cohen-ford-consulting/',
'https://www.motherjones.com/politics/2018/04/misleading-and-unsupported-by-the-facts-house-intelligence-democrats-slam-gop-russia-report/',
'https://www.motherjones.com/politics/2018/03/could-an-ex-russian-operative-and-an-imprisoned-escort-crack-open-the-trump-russia-case/',
'https://www.motherjones.com/politics/2018/05/russia-trump-election-attacks-twitter-facebook-clint-watts/',
'https://www.motherjones.com/politics/2018/04/this-is-what-people-whose-lives-have-been-upended-by-the-travel-ban-want-to-tell-the-supreme-court/',
'https://www.motherjones.com/politics/2018/05/one-of-the-countrys-most-powerful-police-chiefs-is-calling-for-gun-control-after-the-texas-school-shooting/',
'https://www.motherjones.com/politics/2018/04/students-across-the-country-are-walking-out-of-school-to-honor-victims-of-gun-violence/',
'https://www.motherjones.com/politics/2018/04/democrats-are-asking-two-sandy-hook-parents-to-run-for-congress-its-not-an-easy-decision/',
'https://www.motherjones.com/politics/2018/04/despite-the-trump-administrations-declarations-theres-no-evidence-russia-is-interfering-in-mexicos-election/',
'https://www.motherjones.com/politics/2018/06/bombshell-letter-trump-jr-congress-testimony/',
'https://www.motherjones.com/politics/2018/03/nightmare-travel-ban-kafkaesque-refugee-gay-1/',
'https://www.motherjones.com/politics/2018/04/in-a-tweet-trump-warns-of-imminent-air-strikes-in-syria-get-ready/',
'https://www.motherjones.com/politics/2018/03/puerto-rico-is-trying-to-overhaul-its-public-schools-and-teachers-are-furious/',
'https://www.motherjones.com/politics/2018/05/arizona-teacher-strike-just-ended-ducey/',
'https://www.motherjones.com/politics/2018/05/don-blankenship-just-lost/',
'https://www.motherjones.com/politics/2018/03/democrats-call-out-trumps-consumer-watchdog-for-letting-payday-lenders-off-the-hook/',
'https://www.motherjones.com/politics/2018/05/the-first-campaign-ad-against-devin-nunes-doesnt-mention-two-big-things/',
'https://www.motherjones.com/politics/2018/05/senate-votes-to-overturn-fccs-net-neutrality-repeal/',
'https://www.motherjones.com/politics/2018/05/donald-trumps-business-empire-is-no-longer-growing/',
'https://www.motherjones.com/politics/2018/05/trump-contradicts-himself-by-claiming-he-didnt-fire-comey-over-russia/',
'https://www.motherjones.com/politics/2018/04/a-texas-oil-giant-wants-justin-trudeau-to-help-it-build-a-controversial-pipeline-through-canada/',
'https://www.motherjones.com/politics/2018/04/more-guns-wont-make-us-safer-heres-what-might/',
'https://www.motherjones.com/politics/2018/05/supreme-court-deals-a-big-blow-to-workers-rights/',
'https://www.motherjones.com/politics/2018/04/this-poll-is-extremely-bad-news-for-ted-cruz/',
'https://www.motherjones.com/politics/2018/05/trump-says-muellers-leaked-questions-dont-involve-collusion-actually-they-do/',
'https://www.motherjones.com/politics/2018/05/russian-journalist-murdered-putin-critic-kiev-arkady-babchenko-alive/',
'https://www.motherjones.com/politics/2018/05/lawmakers-just-might-do-something-positive-for-pregnant-women-for-a-change/',
'https://www.motherjones.com/politics/2018/05/an-amazon-echo-recorded-a-familys-private-conversation-and-sent-it-to-some-random-person/',
'https://www.motherjones.com/politics/2018/04/zuckerberg-clinton-trump-russia-hacker-campaign/',
'https://www.motherjones.com/politics/2018/04/republicans-are-a-no-show-across-the-country-for-town-halls-on-gun-action-forum/',
'https://www.motherjones.com/politics/2018/05/trump-dinesh-dsouza-pardon-announcement/',
'https://www.motherjones.com/politics/2018/03/you-wont-believe-what-ted-nugent-just-said-about-the-parkland-survivors/',
'https://www.motherjones.com/politics/2018/04/the-dnc-just-sued-the-trump-campaign-and-russia-for-collusion/',
'https://www.motherjones.com/politics/2018/05/a-republican-leader-is-switching-districts-but-its-not-at-all-because-hes-terrified-of-a-blue-wave/',
'https://www.motherjones.com/politics/2018/04/the-finance-industry-has-quietly-launched-an-assault-on-state-sponsored-retirement-plans/',
'https://www.motherjones.com/politics/2018/05/savvy-doctors-can-convince-reluctant-parents-to-vaccinate-their-kids/',
'https://www.motherjones.com/politics/2018/05/how-a-tenacious-group-of-puerto-ricans-brought-light-back-to-their-community/',
'https://www.motherjones.com/politics/2018/05/iowa-wants-to-ban-abortions-after-6-weeks-planned-parenthood-just-filed-a-lawsuit-to-stop-it/',
'https://www.motherjones.com/politics/2018/04/new-data-america-schools-suspend-punish-arrest-black-students/',
'https://www.motherjones.com/politics/2018/04/arizona-teacher-walkout-strike-pay-funding-ducey/',
'https://www.motherjones.com/politics/2018/03/devin-nunes-fresno-bee/',
'https://www.motherjones.com/politics/2018/05/the-case-for-building-public-housing-that-doesnt-suck-and-lots-of-it/',
'https://www.motherjones.com/politics/2018/04/trump-calls-on-montana-senator-to-resign-over-ronny-jackson-allegations/',
'https://www.motherjones.com/politics/2018/04/automakers-went-to-incredible-lengths-to-convince-the-epa-to-roll-back-fuel-standards/',
'https://www.motherjones.com/politics/2018/04/fbi-raids-office-of-longtime-trump-lawyer-michael-cohen-trump-response/',
'https://www.motherjones.com/politics/2018/06/betsy-devos-school-safety-commission-guns-leahy-murray/',
'https://www.motherjones.com/politics/2018/03/voting-rights-advocates-just-won-a-big-victory-in-court/',
'https://www.motherjones.com/politics/2018/05/stacey-abrams-just-moved-one-step-closer-to-becoming-americas-first-black-female-governor-1/',
'https://www.motherjones.com/politics/2018/05/two-millennial-socialists-take-down-a-pittsburgh-political-dynasty-1-results/',
'https://www.motherjones.com/politics/2018/05/richard-ojeda-slams-trump/',
'https://www.motherjones.com/politics/2018/05/israel-kills-dozens-of-protesters-as-trumps-family-celebrates-new-jerusalem-embassy/',
'https://www.motherjones.com/politics/2018/05/i-didnt-want-to-watch-dear-white-people-because-i-lived-it/',
'https://www.motherjones.com/politics/2018/04/thousands-of-poor-detroiters-are-about-to-get-their-water-cut-off/',
'https://www.motherjones.com/politics/2018/05/pro-trump-pastor-who-claims-islam-is-a-cult-picked-to-lead-prayer-at-opening-of-us-embassy-in-jerusalem/',
'https://www.motherjones.com/politics/2018/06/california-democrats-districts-congress-primary-results/',
'https://www.motherjones.com/politics/2018/04/it-looks-like-trump-is-actually-sending-to-the-border/',
'https://www.motherjones.com/politics/2018/03/jess-phoenix-steve-knight/',
'https://www.motherjones.com/politics/2018/04/mlk-50/',
'https://www.motherjones.com/politics/2018/04/this-national-enquirer-cover-about-michael-cohen-is-amazing/',
'https://www.motherjones.com/politics/2018/06/supreme-court-ruling-for-anti-gay-marriage-baker-could-spell-bad-news-for-trumps-travel-ban/',
'https://www.motherjones.com/politics/2018/04/if-trump-fires-rosenstein-this-man-could-end-up-with-power-over-the-russia-investigation/',
'https://www.motherjones.com/politics/2018/05/congress-prepares-to-undermine-trump-on-trade/',
'https://www.motherjones.com/politics/2018/04/a-new-study-shows-men-in-science-classes-really-are-arrogant-bastards/',
'https://www.motherjones.com/politics/2018/04/trump-just-pardoned-scooter-libby/',
'https://www.motherjones.com/politics/2018/05/how-two-filmmakers-convinced-rbg-to-let-them-film-her-workout/',
'https://www.motherjones.com/politics/2018/05/rudy-giuliani-trump-subpoena-mueller-cnn-interview/',
'https://www.motherjones.com/politics/2018/04/key-senate-republicans-are-finally-admitting-trump-might-fire-mueller/',
'https://www.motherjones.com/politics/2018/05/trump-threatens-to-get-involved-with-justice-department-rod-rosenstein/',
'https://www.motherjones.com/politics/2018/05/the-fbi-says-your-router-is-helping-russian-hackers/',
'https://www.motherjones.com/politics/2018/04/asylum-seekers-central-american-caravan-turned-away-us-border/',
'https://www.motherjones.com/politics/2018/05/trump-cancels-north-korea-summit-in-open-letter/',
'https://www.motherjones.com/politics/2018/04/all-the-times-this-week-fox-news-used-kanyes-tweets-to-push-its-pro-trump-agenda/',
'https://www.motherjones.com/politics/2018/05/you-may-have-noticed-that-gas-is-more-expensive-this-holiday-weekend/',
'https://www.motherjones.com/politics/2018/06/rudy-giuliani-says-trump-shouldnt-testify-because-our-recollection-keeps-changing/',
'https://www.motherjones.com/politics/2018/04/after-syria-attacks-trump-boasts-mission-accomplished/',
'https://www.motherjones.com/politics/2018/05/key-democrat-will-support-haspels-nomination-for-cia-director-despite-past-connections-to-torture/',
'https://www.motherjones.com/politics/2018/05/big-opioid-distributors-just-had-a-very-bad-day-iin-congress/',
'https://www.motherjones.com/politics/2018/05/jeanine-pirro-has-a-direct-line-into-trumps-brain/',
'https://www.motherjones.com/politics/2018/04/thanks-to-tammy-duckworth-the-senate-just-made-a-historic-change/',
'https://www.motherjones.com/politics/2018/04/in-latest-attack-on-washington-post-trump-takes-a-crack-at-headline-writing/',
'https://www.motherjones.com/politics/2018/05/incumbent-walter-jones-wins-north-carolina-gop-primary/',
'https://www.motherjones.com/politics/2018/04/trump-rages-over-fbi-raids-targeting-his-longtime-lawyer/',
'https://www.motherjones.com/politics/2018/04/pesticide-executives-are-running-ag-policy-for-donald-trump/',
'https://www.motherjones.com/politics/2018/04/exhaustive-history-donald-trump-russia-scandal-timeline/',
'https://www.motherjones.com/politics/2018/03/the-2020-census-is-a-cybersecurity-fiasco-waiting-to-happen/',
'https://www.motherjones.com/politics/2018/03/california-sues-trump-administration-over-census-citizenship-question/',
'https://www.motherjones.com/politics/2018/05/parkland-survivor-calls-trump-a-professional-liar-after-nra-speech/',
'https://www.motherjones.com/politics/2018/05/stacey-adams-bizarre-gerrymandering-controversy/',
'https://www.motherjones.com/politics/2018/05/ali-wong-stuck-with-the-major-your-mom-told-you-to-drop-and-here-she-is-today-hard-knock-wife/',
'https://www.motherjones.com/politics/2018/04/309-women-are-now-running-for-congress-thats-a-record/',
'https://www.motherjones.com/politics/2018/04/watch-this-federal-judicial-nominee-evade-questions-about-whether-planned-parenthood-kills-150000-females-a-year/',
'https://www.motherjones.com/politics/2018/05/new-documents-trump-pushed-hard-for-a-meeting-with-putin-in-2013/',
'https://www.motherjones.com/politics/2018/05/stormy-daniels-lawyer-claims-russian-oligarch-paid-500000-to-michael-cohen-1/',
'https://www.motherjones.com/politics/2018/04/a-top-trump-official-says-syrian-refugees-dont-want-to-come-to-the-us-in-reality-weve-effectively-banned-them/',
'https://www.motherjones.com/politics/2018/04/member-of-trumps-voter-fraud-commission-sued-for-voter-intimidation/',
'https://www.motherjones.com/politics/2018/04/donald-trump-just-changed-his-story-about-james-comeys-firing/',
'https://www.motherjones.com/politics/2018/05/rudy-giuliani-may-have-made-trumps-legal-woes-way-worse/',
'https://www.motherjones.com/politics/2018/06/trudeau-trump-trade-tariffs-interview-nbc-insulting/',
'https://www.motherjones.com/politics/2018/04/trump-administration-imposes-sanctions-on-russian-oligarchs/',
'https://www.motherjones.com/politics/2018/06/trump-asserts-absolute-right-to-pardon-himself-in-russia-probe/',
'https://www.motherjones.com/politics/2018/05/donald-trump-calls-white-house-leakers-traitors-and-vows-to-find-out-who-they-are/',
'https://www.motherjones.com/politics/2018/04/17-states-sue-the-trump-administration-over-census-citizenship-question/',
'https://www.motherjones.com/politics/2018/04/a-major-trump-donor-has-a-crazy-story-to-tell-about-how-the-qataris-hacked-his-email/',
'https://www.motherjones.com/politics/2018/06/trump-manafort-mistakes-david-corn-russia-podcast/',
'https://www.motherjones.com/politics/2018/04/this-is-not-normal-james-comey-responds-to-trumps-jail-threat/',
'https://www.motherjones.com/politics/2018/06/iowa-primaries-jd-scholten-steve-king-trump-tariffs/',
'https://www.motherjones.com/politics/2018/04/paul-ryan-gave-the-house-chaplain-a-simple-choice-resign-or-get-fired/',
'https://www.motherjones.com/politics/2018/04/trumps-pick-to-be-americas-top-diplomat-doesnt-think-gay-marriage-should-be-legal/',
'https://www.motherjones.com/politics/2018/06/supreme-court-rules-in-favor-of-baker-who-refused-to-make-a-gay-wedding-cake/',
'https://www.motherjones.com/politics/2018/05/north-korea-releases-three-detained-americans/',
'https://www.motherjones.com/politics/2018/04/leaked-proposal-shows-trump-administration-planning-to-kill-crucial-protections-for-threatened-animals/',
'https://www.motherjones.com/politics/2018/03/jeff-sessions-wont-appoint-a-second-special-counsel-for-now-1/',
'https://www.motherjones.com/politics/2018/04/ice-agents-feel-more-empowered-than-ever-to-arrest-and-deport-even-the-lowest-priority-immigrants/',
'https://www.motherjones.com/politics/2018/04/ice-cold-how-a-loyal-obama-bureaucrat-became-the-face-of-trumps-deportation-force/',
'https://www.motherjones.com/politics/2018/04/top-trump-fundraiser-resigns-over-hush-deal-he-made-with-an-impregnated-playboy-playmate/',
'https://www.motherjones.com/politics/2018/06/ex-employee-says-nasa-full-of-fear-and-anxiety-since-trump-took-office/',
'https://www.motherjones.com/politics/2018/05/snl-season-finale-puts-a-trumpy-twist-on-the-famous-sopranos-finale/',
'https://www.motherjones.com/politics/2018/05/marco-rubio-is-acting-on-strange-russia-theories-in-latin-america/',
'https://www.motherjones.com/politics/2018/04/trump-says-hes-super-interested-in-a-universal-flu-vaccine-his-budget-says-otherwise/',
'https://www.motherjones.com/politics/2018/04/donald-trump-finally-tweeted-about-stormy-daniels/',
'https://www.motherjones.com/politics/2018/04/heres-how-trump-is-rigging-democracy-at-the-voting-booth/',
'https://www.motherjones.com/politics/2018/05/richard-cordray-beats-dennis-kucinich-in-ohio-democratic-primary/',
'https://www.motherjones.com/politics/2018/05/report-suggests-blackwater-founder-erik-prince-may-have-lied-to-congress/',
'https://www.motherjones.com/politics/2018/03/this-amazing-video-shows-how-local-tv-stations-across-america-are-parroting-pro-trump-propaganda/',
'https://www.motherjones.com/politics/2018/05/oklahoma-republican-governor-fallin-nra/',
'https://www.motherjones.com/politics/2018/06/the-messy-universe-inside-plants-looks-a-lot-like-the-messy-universe-inside-people/',
'https://www.motherjones.com/politics/2018/05/evan-jenkinss-campaign-is-every-bit-as-racist-as-don-blankenships/',
'https://www.motherjones.com/politics/2018/05/trump-just-blew-past-two-deadlines-for-reporting-how-many-civilians-the-us-kills/',
'https://www.motherjones.com/politics/2018/03/conservatives-are-now-mocking-david-hogg-for-getting-rejected-by-some-colleges-laura-ingraham-boycott/',
'https://www.motherjones.com/politics/2018/04/james-comey-had-some-very-not-nice-things-to-say-about-donald-trump/',
'https://www.motherjones.com/politics/2018/04/the-most-important-news-out-of-jim-comeys-explosive-new-book/',
'https://www.motherjones.com/politics/2018/04/jeff-sessions-wont-recuse-himself-from-michael-cohens-case/',
'https://www.motherjones.com/politics/2018/04/trump-tweet-sinclair-cnn/',
'https://www.motherjones.com/politics/2018/04/americas-fentanyl-problem-is-reaching-a-whole-new-group-of-users/',
'https://www.motherjones.com/politics/2018/06/david-koch-stepping-back-from-political-causes/',
'https://www.motherjones.com/politics/2018/05/trump-animals-immigrants-white-house-statement/',
'https://www.motherjones.com/politics/2018/04/james-comey-says-collusion-is-not-the-issue/',
'https://www.motherjones.com/politics/2018/05/the-kentucky-house-majority-leader-wrote-a-bill-to-cut-teachers-pensions-this-week-a-teacher-beat-him-at-the-polls/',
'https://www.motherjones.com/politics/2018/04/who-can-stop-jeff-sessions-from-breaking-his-recusal-pledge-probably-no-one/',
'https://www.motherjones.com/politics/2018/05/giuliani-attempts-to-clean-up-explosive-statements-on-trumps-stormy-daniels-payment/',
'https://www.motherjones.com/politics/2018/05/insys-subsys-whistleblower-lawsuits/',
'https://www.motherjones.com/politics/2018/06/millennials-and-women-and-millennial-women-are-dominating-democratic-primaries/',
'https://www.motherjones.com/politics/2018/06/trump-russia-scandal-media/',
'https://www.motherjones.com/politics/2018/04/something-very-weird-is-happening-in-trumpland-regarding-syria/',
'https://www.motherjones.com/politics/2018/05/trump-russia-investigation-tweet-sorry/',
'https://www.motherjones.com/politics/2018/05/why-mark-twain-would-oppose-gina-haspel-as-cia-director/',
'https://www.motherjones.com/politics/2018/05/with-each-pharma-funded-meal-doctors-opioid-prescriptions-rise/',
'https://www.motherjones.com/politics/2018/05/eric-greitens-missouri-governor-resigns/',
'https://www.motherjones.com/politics/2018/04/trumps-immigration-crackdown-has-separated-hundreds-of-kids-from-their-parents-at-the-border/',
'https://www.motherjones.com/politics/2018/06/paul-manafort-mueller-witness-tampering/',
'https://www.motherjones.com/politics/2018/04/what-exactly-was-corey-lewandowski-just-doing-in-belgrade/',
'https://www.motherjones.com/politics/2018/05/rohrabacher-fine-with-housing-discrimination-against-gay-people/',
'https://www.motherjones.com/politics/2018/05/cambridge-analytica-aleksandr-kogan-ted-cruz/',
'https://www.motherjones.com/politics/2018/04/snl-skewers-mark-zuckerberg-ahead-of-his-trip-to-congress/',
'https://www.motherjones.com/politics/2018/04/lebron-james-donald-trump-laura-ingraham-ali-jordan-robinson/',
'https://www.motherjones.com/politics/2018/05/michael-cohen-met-with-qatari-official-and-nuclear-plant-owner-last-month/',
'https://www.motherjones.com/politics/2018/04/trump-takes-his-anti-immigrant-tweets-to-a-new-level/',
'https://www.motherjones.com/politics/2018/04/trump-is-scaring-the-hell-out-of-his-advisers-right-now/',
'https://www.motherjones.com/politics/2018/05/santa-fe-shooting-parkland-survivors-support-emma-gonzalez-david-hogg/',
'https://www.motherjones.com/politics/2018/05/trump-giuliani-confirms-his-money-paid-for-stormy-danielss-hush-agreement/',
'https://www.motherjones.com/politics/2018/05/a-grim-new-reality-more-overdose-deaths-means-more-available-organs/',
'https://www.motherjones.com/politics/2018/04/doctors-are-required-to-receive-opioid-training-big-pharma-funds-it-what-could-go-wrong/',
'https://www.motherjones.com/politics/2018/06/trump-blames-fbi-for-not-warning-him-about-paul-manafort/',
'https://www.motherjones.com/politics/2018/03/50-years-after-dc-burned-the-injustices-that-caused-the-riots-are-as-urgent-as-ever/',
'https://www.motherjones.com/politics/2018/06/martha-roby-donald-trump-runoff/',
'https://www.motherjones.com/politics/2018/06/disinformation-russian-trolls-twitter-facebook-election-2018/',
'https://www.motherjones.com/politics/2018/05/trumps-immigration-crackdown-is-a-boom-time-for-private-prisons/',
'https://www.motherjones.com/politics/2018/05/federal-government-poorly-prepared-tick-mosquito-borne-diseases/',
'https://www.motherjones.com/politics/2018/04/trump-went-on-fox-friends-this-morning-and-likely-sent-his-lawyers-into-a-meltdown-1/',
'https://www.motherjones.com/politics/2018/05/ebola-is-back-and-trump-just-made-it-harder-to-fight/',
'https://www.motherjones.com/politics/2018/03/the-real-reason-david-shulkin-was-fired-according-to-david-shulkin/',
'https://www.motherjones.com/politics/2018/05/key-arizona-republican-freaks-out-over-another-generation-of-daca-like-people/',
'https://www.motherjones.com/politics/2018/04/michael-browns-mother-is-considering-a-run-for-ferguson-city-council/',
'https://www.motherjones.com/politics/2018/04/trump-calls-for-sending-military-to-the-mexican-border/',
'https://www.motherjones.com/politics/2018/03/a-maryland-judge-just-gave-the-go-ahead-to-a-major-case-against-trump/',
'https://www.motherjones.com/politics/2018/05/most-shocking-gop-nastiest-primary/',
'https://www.motherjones.com/politics/2018/04/theres-a-new-problem-with-trumps-attacks-on-amazon/',
'https://www.motherjones.com/politics/2018/05/donald-trump-capitalizes-poll-numbers/',
'https://www.motherjones.com/politics/2018/04/colorado-teachers-strike-republican-lawmakers-send-them-jail/',
'https://www.motherjones.com/politics/2018/04/read-the-james-comey-memos-about-donald-trump/',
'https://www.motherjones.com/politics/2018/04/sinclair-ceo-anchor-extremists/',
'https://www.motherjones.com/politics/2018/05/arming-teachers-has-already-led-to-a-slew-of-gun-accidents-in-schools/',
'https://www.motherjones.com/politics/2018/04/sexual-harassment-is-rampant-in-congress-1308-former-staff-members-are-demanding-change/',
'https://www.motherjones.com/politics/2018/05/hillary-clinton-talks-about-trump-facts-and-fascism-in-yale-speech/',
'https://www.motherjones.com/politics/2018/06/montanas-gop-just-nominated-an-anti-death-penalty-candidate/',
'https://www.motherjones.com/politics/2018/05/trump-aides-go-where-jack-abramoff-and-tom-delay-went-before/',
'https://www.motherjones.com/politics/2018/05/roger-stone-to-associate-prepare-to-die/',
'https://www.motherjones.com/politics/2018/05/theres-a-700000-case-backlog-in-immigration-courts-jeff-sessions-just-decided-to-pile-on-more/',
'https://www.motherjones.com/politics/2018/04/arizona-teacher-raise-walkout-ducey/',
'https://www.motherjones.com/politics/2018/05/the-trump-administration-is-being-sued-over-a-very-weird-bird/',
'https://www.motherjones.com/politics/2018/05/sessions-calls-for-prosecuting-everyone-who-crosses-the-border-illegally/',
'https://www.motherjones.com/politics/2018/04/trump-wants-wendy-vitter-who-thinks-planned-parenthood-kills-150000-women-a-year-to-be-a-federal-judge/',
'https://www.motherjones.com/politics/2018/05/latest-news-about-donald-trump-jr-tweet-rant-witch-hunt/',
'https://www.motherjones.com/politics/2018/05/i-went-to-an-evangelical-revival-and-it-was-all-about-fighting-racism-and-protecting-lgbt-rights/',
'https://www.motherjones.com/politics/2018/04/donald-trump-went-on-fox-news-and-barked-some-lies-about-fake-news/',
'https://www.motherjones.com/politics/2018/04/white-house-defiant-amid-allegations-jeopardizing-ronny-jacksons-va-nomination/',
'https://www.motherjones.com/politics/2018/04/trump-blames-obama-for-suspected-chemical-attack-in-syria/',
'https://www.motherjones.com/politics/2018/04/did-drinking-give-me-breast-cancer/',
'https://www.motherjones.com/politics/2018/05/a-new-guardian-report-shows-just-how-far-team-trump-would-go-to-discredit-the-iran-deal-1/',
'https://www.motherjones.com/politics/2018/04/cambridge-analytica-whistleblower-says-he-will-cooperate-with-russia-probes/',
'https://www.motherjones.com/politics/2018/05/last-night-showed-why-the-democratic-civil-war-isnt-as-simple-as-you-thought/',
'https://www.motherjones.com/politics/2018/05/trump-fbi-spy-tweets-criminal-deep-state/',
'https://www.motherjones.com/politics/2018/06/california-governor-senate-primary-results-1/',
'https://www.motherjones.com/politics/2018/04/new-lawsuit-targets-epa-over-audit-scott-pruitt-has-tried-to-keep-secret/',
'https://www.motherjones.com/politics/2018/06/california-lgbt-state-ban-travel-adoption-law/',
'https://www.motherjones.com/politics/2018/05/mark-zuckerberg-fielded-questions-in-brussels-today-european-parliamentarians-say-they-didnt-get-answers/',
'https://www.motherjones.com/politics/2018/05/oliver-north-thinks-nra-leaders-are-being-treated-like-black-americans-under-jim-crow/',
'https://www.motherjones.com/politics/2018/03/nba-star-says-stephon-clark-shooting-taught-his-kids-about-police-brutality/',
'https://www.motherjones.com/politics/2018/04/michael-cohen-will-plead-fifth-in-stormy-daniels-lawsuit-2/',
'https://www.motherjones.com/politics/2018/04/this-gun-control-advocate-hoped-to-win-a-seat-in-the-statehouse-after-parkland-shes-thinking-bigger/',
'https://www.motherjones.com/politics/2018/04/these-oklahoma-teens-are-channeling-the-parkland-student-movement-to-demand-better-school-funding/',
'https://www.motherjones.com/politics/2018/04/trump-tried-to-make-a-russian-mma-reality-show-this-week-the-fbi-questioned-its-star/',
'https://www.motherjones.com/politics/2018/05/ugly-feuds-drunken-stupidity-paul-mccartney-and-a-race-that-could-flip-congress/',
'https://www.motherjones.com/politics/2018/04/a-russian-business-associate-of-wilbur-ross-was-just-sanctioned-by-the-trump-administration/',
'https://www.motherjones.com/politics/2018/04/puerto-rico-still-reeling-from-hurricane-maria-is-hit-by-an-island-wide-blackout/',
'https://www.motherjones.com/politics/2018/05/facebook-suspends-200-apps-that-may-have-misused-users-data/',
'https://www.motherjones.com/politics/2018/04/theres-a-growing-movement-to-let-16-year-olds-vote-it-would-change-everything/',
'https://www.motherjones.com/politics/2018/04/russia-says-deadly-chemical-attack-in-syria-never-happened-and-was-faked-by-the-british/',
'https://www.motherjones.com/politics/2018/05/stormy-daniels-on-saturday-night-live-is-absolutely-perfect/',
'https://www.motherjones.com/politics/2018/05/trump-is-now-fundraising-off-conspiracy-theory-that-fbi-infiltrated-his-campaign/',
'https://www.motherjones.com/politics/2018/04/enraged-by-comey-memos-trump-defends-michael-flynn/',
'https://www.motherjones.com/politics/2018/03/donald-trump-rigging-2020-census-undercounting-minorities-1/',
'https://www.motherjones.com/politics/2018/05/texas-lieutenant-governor-uncovers-the-cause-of-mass-shootings-abortion/',
'https://www.motherjones.com/politics/2018/05/rod-rosenstein-on-threats-to-impeach-him-the-justice-department-is-not-going-to-be-extorted/',
'https://www.motherjones.com/politics/2018/06/one-of-americas-biggest-genetic-testing-companies-refuses-to-publicly-share-data-that-could-save-countless-lives/',
'https://www.motherjones.com/politics/2018/05/white-house-open-to-sanctioning-european-companies-that-do-business-with-iran/',
'https://www.motherjones.com/politics/2018/05/trump-jeff-sessions-attacks-mueller-investigation/',
'https://www.motherjones.com/politics/2018/04/no-one-knows-how-immigration-affects-wages-and-jobs-especially-donald-trump/',
'https://www.motherjones.com/politics/2018/05/as-a-kid-she-petitioned-congress-for-the-right-to-fly-fighter-planes-now-shes-gunning-for-a-seat-of-her-own/',
'https://www.motherjones.com/politics/2018/04/donald-trump-rages-at-former-fbi-director-james-comey/',
'https://www.motherjones.com/politics/2018/03/donald-trump-is-live-tweeting-fox-news-again/',
'https://www.motherjones.com/politics/2018/04/democrats-think-theyre-poised-for-huge-victories-in-these-10-states/',
'https://www.motherjones.com/politics/2018/04/did-trump-jr-talk-to-his-dad-about-the-trump-tower-meeting/',
'https://www.motherjones.com/politics/2018/05/researchers-just-found-the-key-to-your-well-being-and-its-not-money/',
'https://www.motherjones.com/politics/2018/05/mueller-is-asking-questions-about-trumps-inaugural-fund-theres-a-lot-to-investigate-there/',
'https://www.motherjones.com/politics/2018/06/love-contractually-why-unconventional-families-should-put-it-in-writing-lgbt-adoption-parenting/',
'https://www.motherjones.com/politics/2018/05/this-man-was-trump-before-trump-he-just-won-pennsylvanias-senate-primary/',
'https://www.motherjones.com/politics/2018/05/trump-announces-the-us-will-withdraw-from-the-iran-nuclear-deal/',
'https://www.motherjones.com/politics/2018/04/trump-hails-ronny-jackson-as-an-american-hero/',
'https://www.motherjones.com/politics/2018/04/puerto-rico-plans-to-shutter-283-schools/',
'https://www.motherjones.com/politics/2018/03/as-advertisers-bail-fox-news-laura-ingraham-announces-vacation/',
'https://www.motherjones.com/politics/2018/05/this-map-depicts-abortion-access-across-america-and-its-really-bleak/',
'https://www.motherjones.com/politics/2018/05/what-if-we-held-a-constitutional-convention-and-the-right-wingers-prevailed/',
'https://www.motherjones.com/politics/2018/03/you-need-to-calm-down-and-other-degrading-b-s-women-hear-from-doctors/',
'https://www.motherjones.com/politics/2018/05/trump-roseanne-tweet/',
'https://www.motherjones.com/politics/2018/04/pruitt-epa-gao-violated-law-phone-booth/',
'https://www.motherjones.com/politics/2018/04/zuckerberg-confirms-facebook-is-cooperating-with-mueller/',
'https://www.motherjones.com/politics/2018/05/how-your-health-insurer-and-your-doctors-scheme-to-screw-you-over/',
'https://www.motherjones.com/politics/2018/05/rev-william-barber-is-reviving-mlks-poor-peoples-campaign-he-got-arrested-the-first-day-of-protests/',
'https://www.motherjones.com/politics/2018/06/kris-kobach-parade-machine-gun/',
'https://www.motherjones.com/politics/2018/05/china-has-stopped-buying-american-soybeans/',
'https://www.motherjones.com/politics/2018/06/california-democrats-jungle-primary/',
'https://www.motherjones.com/politics/2018/04/a-new-bill-would-give-dc-high-schoolers-the-right-to-vote/',
'https://www.motherjones.com/politics/2018/05/donald-trumps-attacks-on-the-justice-system-are-helping-don-blankenships-campaign/',
'https://www.motherjones.com/politics/2018/05/scott-pruitt-broke-bread-with-a-climate-skeptic-cardinal-accused-of-sexual-abuse/',
'https://www.motherjones.com/politics/2018/04/the-trump-administration-backs-down-from-battle-over-legal-pot/',
'https://www.motherjones.com/politics/2018/03/john-dowd-reportedly-floated-the-idea-of-pardoning-manafort-and-flynn/',
'https://www.motherjones.com/politics/2018/04/trumps-travel-ban-was-supposed-to-allow-exceptions-that-hasnt-really-happened/',
'https://www.motherjones.com/politics/2018/04/guns-were-a-huge-part-of-my-life-growing-up-should-we-talk-about-them-differently-now/',
'https://www.motherjones.com/politics/2018/05/cambridge-analytica-fbi-justice-department/',
'https://www.motherjones.com/politics/2018/04/rutgers-university-report-quality-preschools-kids-success-trump-administration-wants-to-cut-funding/',
'https://www.motherjones.com/politics/2018/04/kentuckys-governor-just-apologized-for-claiming-teacher-protest-led-to-sexual-assaults/',
'https://www.motherjones.com/politics/2018/05/i-was-directed-to-market-oxycontin-a-purdue-pharma-rep-tells-how-he-was-paid-to-push-opioids/',
'https://www.motherjones.com/politics/2018/03/how-jared-kushner-landed-in-the-middle-of-a-vicious-proxy-war-between-qatar-and-its-neighbors/',
'https://www.motherjones.com/politics/2018/05/ignorance-is-strength-the-trump-administrations-creepy-war-on-language/',
'https://www.motherjones.com/politics/2018/05/the-nra-is-still-dodging-questions-on-its-russia-connection/',
'https://www.motherjones.com/politics/2018/05/republican-senate-candidates-want-to-fire-robert-mueller/',
'https://www.motherjones.com/politics/2018/05/enough-is-enough-heres-what-parkland-parents-are-saying-about-the-texas-massacre/',
'https://www.motherjones.com/politics/2018/05/trump-tweets-puerto-rico-hurricane-maria/',
'https://www.motherjones.com/politics/2018/04/trump-ordered-missile-strike-starts-to-hit-damascus/',
'https://www.motherjones.com/politics/2018/05/feds-charge-pac-operators-with-conspiring-to-defraud-conservative-donors/',
'https://www.motherjones.com/politics/2018/04/trumps-plan-to-dismantle-daca-just-hit-a-major-setback-1/',
'https://www.motherjones.com/politics/2018/05/this-ex-con-coal-baron-is-reportedly-within-striking-distance-of-west-virginias-gop-senate-nomination/',
'https://www.motherjones.com/politics/2018/06/trump-north-korea-letter-woops-what-letter/',
'https://www.motherjones.com/politics/2018/05/her-family-is-in-mexico-they-only-had-4-minutes-together-at-the-border-thats-when-he-proposed/',
'https://www.motherjones.com/politics/2018/05/he-voted-for-trump-now-hes-running-for-congress-as-a-pro-pot-pro-coal-democrat/',
'https://www.motherjones.com/politics/2018/04/trump-tower-has-its-second-fire-of-the-year/',
'https://www.motherjones.com/politics/2018/05/change-does-happen-justice-gets-served-stories-that-show-not-all-news-is-grim/',
'https://www.motherjones.com/politics/2018/04/maryland-just-took-a-huge-step-for-protecting-voting-rights-automatic-registration/',
'https://www.motherjones.com/politics/2018/04/facebook-data-breach-cambridge-analytica/',
'https://www.motherjones.com/politics/2018/05/kirstjen-nielsen-trump-russia-interference-intelligence-assessment/',
'https://www.motherjones.com/politics/2018/04/facebook-is-still-the-perfect-propaganda-platform-these-sketchy-mexican-pages-show-why/',
'https://www.motherjones.com/politics/2018/05/donald-trump-jr-trump-tower-june-meeting-senate-transcripts/',
'https://www.motherjones.com/politics/2018/04/kris-kobach-held-in-contempt-of-court/',
'https://www.motherjones.com/politics/2018/05/the-republican-primary-in-georgia-is-taking-racism-to-a-whole-new-level/',
'https://www.motherjones.com/politics/2018/05/how-a-court-ruling-on-joe-arpaio-could-undermine-civil-rights-and-the-mueller-investigation/',
'https://www.motherjones.com/politics/2018/05/trump-nfl-national-anthem-protests-kneeling-shouldnt-be-in-country-fox/',
'https://www.motherjones.com/politics/2018/04/james-comey-leaked-memoir-donald-trump-obsessed-with-pee-tape/',
'https://www.motherjones.com/politics/2018/05/trump-twitter-account-block-unconstitutional-first-amendment/',
'https://www.motherjones.com/politics/2018/04/ice-chief-thomas-homan-the-leader-of-trumps-deportation-force-is-stepping-down/',
'https://www.motherjones.com/politics/2018/05/ireland-just-voted-to-legalize-abortion1/',
'https://www.motherjones.com/politics/2018/04/america-has-never-had-a-black-woman-governor-stacey-abrams-has-something-to-say-about-that/',
'https://www.motherjones.com/politics/2018/04/a-bipartisan-group-of-senators-just-scored-a-big-win-in-the-fight-to-protect-robert-mueller/',
'https://www.motherjones.com/politics/2018/04/barack-obama-sits-down-with-john-lewis-to-discuss-mlks-legacy-and-the-power-of-activism/',
'https://www.motherjones.com/politics/2018/04/trump-threatens-foreign-aid-to-honduras-in-latest-anti-immigrant-tweets/',
'https://www.motherjones.com/politics/2018/04/see-how-hard-it-is-for-sen-bob-corker-to-say-something-nice-about-the-woman-who-might-replace-him/',
'https://www.motherjones.com/politics/2018/04/how-trump-turned-tax-day-into-a-giveaway-for-the-1-percent/',
'https://www.motherjones.com/politics/2018/04/betsy-devos-is-making-it-easier-for-schools-to-send-black-kids-like-this-13-year-old-girl-to-jail/',
'https://www.motherjones.com/politics/2018/05/qatari-investor-accused-in-bribery-plot-appears-with-michael-cohen-in-picture-posted-by-stormy-daniels-lawyer/',
'https://www.motherjones.com/politics/2018/04/ted-cruzs-blurb-on-trump-as-one-of-times-most-100-influential-people-is-something/',
'https://www.motherjones.com/politics/2018/04/justice-department-ig-andrew-mccabe-lacked-candor-1/',
'https://www.motherjones.com/politics/2018/06/trumps-eagles-celebration-of-america-features-his-unfamiliarity-with-god-bless-america/',
'https://www.motherjones.com/politics/2018/04/support-is-mounting-on-the-right-for-trump-to-win-the-nobel-peace-prize/',
'https://www.motherjones.com/politics/2018/04/house-intelligence-committee-republicans-just-released-their-russia-report/',
'https://www.motherjones.com/politics/2018/04/republican-candidate-wins-open-arizona-congressional-seat/',
'https://www.motherjones.com/politics/2018/04/new-research-on-disciplining-children-will-make-you-better-parent-and-spouse/',
'https://www.motherjones.com/politics/2018/05/new-york-attorney-general-eric-schneiderman-resigns-hours-after-allegations-emerge-of-physical-abuse/',
'https://www.motherjones.com/politics/2018/05/heres-how-the-special-prosecutor-will-go-after-eric-schneiderman/',
'https://www.motherjones.com/politics/2018/04/rep-dana-rohrabacher-links-youtube-shooting-to-criminal-illegal-aliens/',
'https://www.motherjones.com/politics/2018/05/fundraiser-or-friendly-dinner-the-congressman-planning-puerto-ricos-fiscal-future-would-rather-not-talk-about-it/',
'https://www.motherjones.com/politics/2018/04/how-a-mysterious-overseas-shell-company-used-a-former-gop-congressman-to-lobby-trump-and-congress/',
'https://www.motherjones.com/politics/2018/03/the-white-house-is-lying-about-the-census/',
'https://www.motherjones.com/politics/2018/04/new-york-to-restore-voting-rights-to-thousands-of-ex-felons/',
'https://www.motherjones.com/politics/2018/04/married-immigrants-seeking-green-cards-are-now-targets-for-deportation/',
'https://www.motherjones.com/politics/2018/04/youll-probably-never-save-as-many-lives-as-this-guy-who-got-the-philippines-to-stop-using-lead-paint/',
'https://www.motherjones.com/politics/2018/05/fuck-the-nra-congressional-candidate-swears-in-new-ad/',
'https://www.motherjones.com/politics/2018/05/the-trump-administration-just-took-a-big-step-toward-defunding-planned-parenthood/',
'https://www.motherjones.com/politics/2018/04/trump-blasts-vetting-process-media-for-troubled-va-pick-thats-not-how-it-works/',
'https://www.motherjones.com/politics/2018/05/this-is-your-banking-system-on-trump/',
'https://www.motherjones.com/politics/2018/04/a-federal-court-just-thwarted-trumps-efforts-to-punish-sanctuary-cities-1/',
'https://www.motherjones.com/politics/2018/04/donald-trump-was-sued-for-violating-a-key-part-of-martin-luther-king-jr-s-legacy/',
'https://www.motherjones.com/politics/2018/04/i-will-never-drink-again/',
'https://www.motherjones.com/politics/2018/05/on-anniversary-of-muellers-appointment-trump-calls-the-probe-a-witch-hunt/',
'https://www.motherjones.com/politics/2018/05/this-developer-just-won-a-fight-to-make-california-a-massive-coal-exporter/',
'https://www.motherjones.com/politics/2018/04/immigrant-detainees-claim-they-were-forced-to-clean-bathrooms-to-pay-for-their-own-toilet-paper/',
'https://www.motherjones.com/politics/2018/05/new-study-debunks-a-popular-anti-abortion-argument/',
'https://www.motherjones.com/politics/2018/05/russian-firm-indicted-for-election-interference-accuses-us-of-hypocrisy/',
'https://www.motherjones.com/politics/2018/05/trump-releases-financial-disclosure-form-officially-recognizing-michael-cohen-payment/',
'https://www.motherjones.com/politics/2018/05/seinfeld-jason-alexander-ad-rohrabacher/',
'https://www.motherjones.com/politics/2018/04/trump-was-supposed-to-talk-about-tax-cuts-we-got-rape-immigrants-and-voter-fraud-instead/',
'https://www.motherjones.com/politics/2018/04/thousands-of-teachers-in-red-states-are-leading-the-charge-for-better-school-funding/',
'https://www.motherjones.com/politics/2018/04/james-comey-tells-stephen-colbert-that-trump-cant-get-over-him/',
'https://www.motherjones.com/politics/2018/04/defending-travel-ban-trump-lawyer-says-an-anti-semitic-president-could-ban-israelis/',
'https://www.motherjones.com/politics/2018/05/gina-haspel-trumps-nominee-to-head-the-cia-wont-say-if-torture-is-immoral/',
'https://www.motherjones.com/politics/2018/05/elizabeth-warrens-congress-katie-porter-california-orange-county/',
'https://www.motherjones.com/politics/2018/05/trumps-latest-tweet-just-crossed-another-bright-line/',
'https://www.motherjones.com/politics/2018/05/democratic-senator-demands-investigation-into-whether-trump-jr-lied-to-congress/',
'https://www.motherjones.com/politics/2018/04/how-jerry-falwell-jr-transformed-liberty-university-into-a-wildly-profitable-online-empire/',
'https://www.motherjones.com/politics/2018/05/texas-governor-who-recently-blamed-gun-violence-on-godlessness-now-says-hell-do-something/',
'https://www.motherjones.com/politics/2018/04/one-of-congress-most-unpopular-republicans-might-not-even-have-a-democratic-opponent-in-november/',
'https://www.motherjones.com/politics/2018/05/obama-blasts-trumps-misguided-decision-to-withdraw-from-iran-deal/',
'https://www.motherjones.com/politics/2018/05/nra-oliver-north-iran-contra/',
'https://www.motherjones.com/politics/2018/06/does-forced-rehab-work/',
'https://www.motherjones.com/politics/2018/04/michael-cohen-says-hes-never-been-to-prague-he-told-me-a-different-story/',
'https://www.motherjones.com/politics/2018/05/betsy-devos-wont-go-after-for-profit-college-ripoffs-will-states-step-in/',
'https://www.motherjones.com/politics/2018/04/its-sunday-morning-so-trump-is-tweet-yelling-at-his-tv-again-this-time-about-north-korea/',
'https://www.motherjones.com/politics/2018/04/black-students-are-way-more-likely-to-be-suspended-the-trump-administration-doesnt-seem-to-care/',
'https://www.motherjones.com/politics/2018/05/columbus-nova-michael-cohen/',
'https://www.motherjones.com/politics/2018/04/rand-paul-reverses-himself-agrees-to-support-mike-pompeo/',
'https://www.motherjones.com/politics/2018/05/trump-tweets-about-young-and-beautiful-lives-destroyed-by-russia-investigation/',
'https://www.motherjones.com/politics/2018/05/trump-promised-his-appointees-wouldnt-become-lobbyists-guess-how-that-turned-out/',
'https://www.motherjones.com/politics/2018/04/trump-threatens-comey-with-jail-time-in-unhinged-tirade/'])

def get_article(url):
#Sends request for url
    html = requests.get(url).text
    return html

def parse_article(html):
#BeautifulSoups the article
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h1', class_='entry-title').text
    body = soup.find('article', class_='entry-content').text

    article = {
        'title': title,
        'body': body,
        'source': 'Mother Jones',
        'num_source': 9
    }

    return article

def get_parsed_article_from_link(url):
#Runs the previous two functions on the url
    return parse_article(get_article(url))

#phase 1: uses request to try to BeautifulSoup links
mj_list_o_articles = []
mj_problem_articles = []
for text in mj_first_articles:
    #print(text)
    try:
        art = get_parsed_article_from_link(text.encode())
        mj_list_o_articles.append(art)

    except:
        print("Problem processing url " + text)
        problem = text
        mj_problem_articles.append(problem)
    time.sleep(2)

#phase 2: uses selenium to go through links
driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
for x in mj_problem_articles:
    try:
        driver.get(x)
        time.sleep(3)
        soupy = BeautifulSoup(driver.page_source, 'lxml')
        title = soupy.find('h1', class_='entry-title').text
        body = soupy.find('article', class_='entry-content').text

        articley = {
        'title': title,
        'body': body,
        'source': 'Mother Jones',
        'num_source': 9
        }
        mj_list_o_articles.append(articley)
    except:
        pass
#Same as above but for expanded list, phase 1
mj_more_list_o_articles = []
mj_more_problem_articles = []
for text in mj_more_articles:
    #print(text)
    try:
        art = get_parsed_article_from_link(text.encode())
        mj_more_list_o_articles.append(art)

    except:
        print("Problem processing url " + text)
        problem = text
        mj_more_problem_articles.append(problem)
    time.sleep(2)
#same as above for expanded list, phase 2
driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
for x in mj_more_problem_articles:
    try:
        driver.get(x)
        time.sleep(3)
        soupy = BeautifulSoup(driver.page_source, 'lxml')
        title = soupy.find('h1', class_='entry-title').text
        body = soupy.find('article', class_='entry-content').text

        articley = {
        'title': title,
        'body': body,
        'source': 'Mother Jones',
        'num_source': 9
        }
        mj_more_list_o_articles.append(articley)
    except:
        pass
#puts articles all into one list
all_articles = mj_list_o_articles + mj_more_list_o_articles
#starts client in Mongodb
client = MongoClient()
biased_news = client.project5.biased_news
#creates event and loads articles into Mongodb
db = client.events
biased_news = db.biased_news
biased_news.insert_many(all_articles)
