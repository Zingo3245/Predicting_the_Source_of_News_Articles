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

actpost_first_articles = ['https://www.activistpost.com/2018/06/google-quits-drone-program-u-s-navy-wants-drone-motherships-with-help-of-a-i.html',
 'https://www.activistpost.com/2018/06/conspiracy-theory-proven-fact-as-cops-remove-senator-from-walmart-converted-into-detention-center.html',
 'https://www.activistpost.com/2018/06/something-unprecedented-is-happening-at-bilderberg-2018.html',
 'https://www.activistpost.com/2018/06/cell-phone-companies-warning-shareholders-not-customers-about-health-risks-and-potential-lawsuits-based-on-harm-caused-by-cell-phone-and-wifi-radiation-exposure.html',
 'https://www.activistpost.com/2018/06/connected-cars-can-lie-posing-a-new-threat-to-smart-cities.html',
 'https://www.activistpost.com/2018/06/eye-in-the-sky-drone-surveillance-detect-violence.html',
 'https://www.activistpost.com/2018/06/texas-gold-depository-open-for-business.html',
 'https://www.activistpost.com/2018/06/mit-creates-serial-killer-a-i-personality-with-reddit-experiment.html',
 'https://www.activistpost.com/2018/06/hart-homeland-securitys-massive-new-database-will-include-face-recognition-dna-and-non-obvious-relationships.html',
 'https://www.activistpost.com/2018/06/israeli-selling-surveillance-systems-governments-around-world.html',
 'https://www.activistpost.com/2018/06/commercial-for-asthma-medication-features-unsafe-use-of-technology-respiratory-health-is-affected-by-cell-phone-and-wifi-radiation-and-electrical-pollution-electrosmog.html',
 'https://www.activistpost.com/2018/06/as-media-hypes-trump-kim-summit-the-real-rulers-of-the-world-are-secretly-meeting-at-bilderberg.html',
 'https://www.activistpost.com/2018/06/depression-could-cell-phone-and-wifi-radiation-disrupting-the-blood-brain-barrier-be-playing-a-role.html',
 'https://www.activistpost.com/2018/06/media-silent-as-israel-exposed-for-aiding-saudi-arabia-in-developing-nuclear-weapons.html']
actpost_more_articles = ['https://www.activistpost.com/2018/04/1986-cia-document-analyzes-possibilities-of-regime-change-in-syria.html',
 'https://www.activistpost.com/2018/04/bill-gates-warns-of-coming-apocalyptic-disease-pledges-12-million-to-universal-vaccine.html',
 'https://www.activistpost.com/2018/05/israel-complains-syria-is-defending-itself.html',
 'https://www.activistpost.com/2018/05/us-history-attempting-overthrow-iran-riddled-with-conspiracy-to-stage-conflicts-disbandthecia.html',
 'https://www.activistpost.com/2018/04/in-2011-ohios-dennis-kucinich-spoke-about-harm-from-exposure-to-cell-phones-and-cell-towers-so-where-does-he-stand-now-on-bills-which-allow-small-cell-towers-in-yards.html',
 'https://www.activistpost.com/2018/05/study-of-91000links-nighttime-phone-use-with-mental-health-disorders-decades-of-research-says-cell-phone-and-wifi-radiation-exposure-can-cause-same-disorders-24-7.html',
 'https://www.activistpost.com/2018/04/town-bypasses-constitution-us-citizens-given-60-days-to-turn-in-guns-or-become-criminals.html',
 'https://www.activistpost.com/2018/06/study-reveals-45-of-american-teens-are-online-almost-constantly-research-reveals-software-and-wifi-radiation-causes-addicted-behavior.html',
 'https://www.activistpost.com/2018/04/frying-ohio-dr-oz-environmentalists-scientists-security-experts-concerned-about-4g-5g-towers-ohio-officials-voting-to-install-them-in-yards-and-everywhere-else.html',
 'https://www.activistpost.com/2018/05/the-coming-of-an-apocalyptic-disease.html',
 'https://www.activistpost.com/2018/04/smart-city-projects-are-really-police-cam-share-programs-in-disguise.html',
 'https://www.activistpost.com/2018/05/us-france-uk-establish-more-bases-in-syria-to-push-breakup-of-country.html',
 'https://www.activistpost.com/2018/06/helpful-guide-to-stop-5g-small-cell-towers-from-being-installed-in-residential-yards-throughout-your-community.html',
 'https://www.activistpost.com/2018/04/russia-blocks-millions-ip-addresses-including-local-businesses-over-telegram-refusing-encryption-keys.html',
 'https://www.activistpost.com/2018/05/would-you-know-a-small-cell-tower-if-you-saw-one-hundreds-of-thousands-have-already-been-installed-millions-more-are-on-their-way.html',
 'https://www.activistpost.com/2018/05/famous-people-concerned-about-cell-phone-and-wifi-radiation-include-bill-maher-dr-oz-jill-stein-gwyneth-paltrow-suzanne-somers-kourtney-kardashian-lady-gaga.html',
 'https://www.activistpost.com/2018/05/according-to-cisco-there-are-3-reasons-why-almost-75-of-internet-of-things-iot-projects-fail-so-why-are-taxpayer-dollars-still-being-spent-to-connect-everything-to-it.html',
 'https://www.activistpost.com/2018/04/zuckerberg-admits-hes-developing-artificial-intelligence-to-censor-content.html',
 'https://www.activistpost.com/2018/05/96-year-old-wwii-vet-in-a-wheelchair-groped-and-molested-by-tsa-for-freedom.html',
 'https://www.activistpost.com/2018/04/international-human-rights-commission-drops-the-ball-in-medical-kidnap-pleas.html',
 'https://www.activistpost.com/2018/06/u-s-labor-market-reports-someone-is-lying.html',
 'https://www.activistpost.com/2018/05/trump-goes-full-neocon-as-bolton-adds-fred-fleitz-as-nsc-chief-of-staff.html',
 'https://www.activistpost.com/2018/04/silver-may-be-getting-ready-to-shine-again.html',
 'https://www.activistpost.com/2018/04/dailymail-shows-how-easy-it-is-to-steal-a-car-and-amazon-ebay-others-are-selling-the-tools.html',
 'https://www.activistpost.com/2018/04/man-sentenced-to-8-months-in-prison-after-flipping-off-a-red-light-camera.html',
 'https://www.activistpost.com/2018/05/new-data-shows-police-state-facial-recognition-is-wrong-over-90-of-the-time.html',
 'https://www.activistpost.com/2018/04/when-the-president-wants-to-leave-syria-and-the-deep-state-doesnt.html',
 'https://www.activistpost.com/2018/03/2018-2028-the-most-dangerous-decade.html',
 'https://www.activistpost.com/2018/06/environmental-groups-sue-trump-administration-for-abandoning-investigation-into-dangerous-pesticides.html',
 'https://www.activistpost.com/2018/05/npr-continues-coverage-of-wireless-wifi-radiation-health-risks-and-how-big-wireless-made-us-think-that-cell-phones-are-safe.html',
 'https://www.activistpost.com/2018/04/bill-gates-funding-satellites-global-real-time-surveillance.html',
 'https://www.activistpost.com/2018/06/something-unprecedented-is-happening-at-bilderberg-2018.html',
 'https://www.activistpost.com/2018/05/war-on-cash-goes-into-full-effect-purchases-over-10000-illegal-in-australia.html',
 'https://www.activistpost.com/2018/04/6-reasons-to-get-out-of-afghanistan.html',
 'https://www.activistpost.com/2018/05/artificial-intelligence-how-much-are-you-affected-by-it.html',
 'https://www.activistpost.com/2018/05/federal-reserve-note-dances-upon-its-own-grave.html',
 'https://www.activistpost.com/2018/04/you-dont-have-to-be-a-scientist-to-say-that-cell-phone-and-wifi-radiation-are-harmful-the-world-health-organization-and-other-scientists-have-already-said-it-for-you.html',
 'https://www.activistpost.com/2018/05/russia-china-and-iran-counter-donald-trumps-removal-of-the-u-s-from-iran-deal.html',
 'https://www.activistpost.com/2018/05/state-sets-massive-precedent-passes-law-to-effectively-ban-the-nsa.html',
 'https://www.activistpost.com/2018/05/lawmakers-introduce-farm-bill-amendment-to-prohibit-federal-government-interference-in-raw-milk-sales.html',
 'https://www.activistpost.com/2018/05/james-comey-says-deep-state-doesnt-exist-then-describes-the-deep-states-existence.html',
 'https://www.activistpost.com/2018/06/pink-floyd-frontman-opens-show-by-exposing-the-government-silencing-of-julian-assange.html',
 'https://www.activistpost.com/2018/06/watch-live-trust-in-satoshis-vision-with-derek-magill-of-nakamoto-studies-institute.html',
 'https://www.activistpost.com/2018/05/1984-the-uk-is-illegally-detaining-two-journalists-seemingly-making-them-vanish.html',
 'https://www.activistpost.com/2018/05/families-of-mk-ultra-victims-file-lawsuit-over-government-mind-control-experiments.html',
 'https://www.activistpost.com/2018/05/us-claims-of-russian-meddling-exposes-its-own-global-meddling.html',
 'https://www.activistpost.com/2018/04/time-to-expose-md-julie-gerberding-former-cdc-director-for-her-role-in-cdcs-vaccine-fraud.html',
 'https://www.activistpost.com/2018/04/worlds-first-bank-entirely-run-by-robots-opens-up-in-china.html',
 'https://www.activistpost.com/2018/04/dhs-thinks-wearing-black-means-you-may-be-an-anarchist.html',
 'https://www.activistpost.com/2018/06/amazons-rekognition-surveillance-tool-will-grant-police-even-more-surveillance-power.html',
 'https://www.activistpost.com/2018/04/chinas-social-credit-system-sounds-pretty-dystopian-but-are-we-far-behind.html',
 'https://www.activistpost.com/2018/06/factual-microwave-radiation-research-consumers-need-to-know-before-embracing-5g.html',
 'https://www.activistpost.com/2018/04/senators-call-on-homeland-security-to-release-info-on-d-c-cellphone-surveillance.html',
 'https://www.activistpost.com/2018/05/facebook-begins-ranking-news-sites-by-trust-and-combating-propaganda-during-elections.html',
 'https://www.activistpost.com/2018/05/mattis-we-maintain-military-optionsiran-can-never-acquire-a-nuclear-weapon.html',
 'https://www.activistpost.com/2018/06/50-years-after-rfk-was-killed-here-are-5-reasons-why-his-own-son-doesnt-believe-the-official-story.html',
 'https://www.activistpost.com/2018/06/california-senate-passes-bill-to-create-banking-alternative-for-cannabis-industry-bypass-federal-reserve.html',
 'https://www.activistpost.com/2018/05/leaks-fake-news-hidden-agendas-analyzing-mainstream-news-anti-logic.html',
 'https://www.activistpost.com/2018/05/israel-setting-the-stage-to-attack-iran-over-phony-claims-of-iranian-missile-threats.html',
 'https://www.activistpost.com/2018/05/top-five-reasons-to-vote-with-your-feet.html',
 'https://www.activistpost.com/2018/05/gold-eagle-sales-still-faltering-while-mining-output-collapses-perfect-storm.html',
 'https://www.activistpost.com/2018/04/the-value-and-importance-of-volunteering.html',
 'https://www.activistpost.com/2018/04/debunking-10-lies-about-syria-and-assad.html',
 'https://www.activistpost.com/2018/03/how-the-cia-hid-their-mkultra-mind-control-program.html',
 'https://www.activistpost.com/2018/05/why-america-is-the-greatest-country.html',
 'https://www.activistpost.com/2018/05/charity-worker-arrested-facing-5-years-in-prison-for-giving-starving-immigrants-food-and-water.html',
 'https://www.activistpost.com/2018/03/microsoft-warns-customers-watch-what-you-say-when-using-our-products-or-else.html',
 'https://www.activistpost.com/2018/05/why-limit-your-kids-screen-time-anxiety-depression-eye-strain-insomnia-add-adhd-delayed-maturity-cancer-risk-text-neck-diabetes-obesity-digital-addiction-infertility.html',
 'https://www.activistpost.com/2018/04/before-attacking-syria-lets-remember-the-last-country-we-liberated-from-an-evil-dictator.html',
 'https://www.activistpost.com/2018/05/dear-diabetics-videotaped-research-study-demonstrates-how-using-treadmills-can-mess-with-your-blood-sugar-levels.html',
 'https://www.activistpost.com/2018/04/is-there-really-such-a-thing-as-remote-mind-control.html',
 'https://www.activistpost.com/2018/05/silvers-long-consolidation-looks-like-a-launching-pad.html',
 'https://www.activistpost.com/2018/04/syria-a-case-study-in-propaganda.html',
 'https://www.activistpost.com/2018/05/federal-appeals-court-in-virginia-rules-feds-cannot-search-electronic-devices-without-warrant.html',
 'https://www.activistpost.com/2018/04/u-s-citizens-fund-un-arms-trade-treaty-which-impacts-u-s-gun-ownership.html',
 'https://www.activistpost.com/2018/04/how-the-cias-secret-torture-program-sparked-a-citizen-led-public-reckoning-in-north-carolina.html',
 'https://www.activistpost.com/2018/03/the-personal-data-google-has-on-you-is-shocking-dwarfs-that-of-facebook-heres-how-to-stop-it.html',
 'https://www.activistpost.com/2018/04/viral-video-exposes-news-stations-across-us-pumping-exact-same-scripted-fear-into-viewers.html',
 'https://www.activistpost.com/2018/05/book-the-confidence-code-for-girls-encourages-more-risk-taking-less-people-pleasing-how-long-before-more-of-us-are-confident-in-speaking-against-harm-caused-by-technology.html',
 'https://www.activistpost.com/2018/06/foia-request-reveals-femas-egregious-million-dollar-spending-on-a-floating-hotel-as-hurricane-victims-suffered.html',
 'https://www.activistpost.com/2018/05/former-cia-analyst-turned-activist-ray-mcgovern-escorted-out-of-gina-haspel-cia-confirmation-hearing.html',
 'https://www.activistpost.com/2018/04/police-use-corporate-public-safety-apps-to-spy-on-everyone.html',
 'https://www.activistpost.com/2018/05/cops-raid-little-boys-lemonade-stand-shut-it-down-for-not-having-a-permit.html',
 'https://www.activistpost.com/2018/06/mainstream-fake-news-the-devious-limited-hangout.html',
 'https://www.activistpost.com/2018/04/the-government-cant-find-20-trillion-while-pension-funds-are-tanking.html',
 'https://www.activistpost.com/2018/04/supreme-court-rules-cops-can-kill-non-threatening-people-as-long-as-they-say-they-were-scared.html',
 'https://www.activistpost.com/2018/05/failed-false-flag-anti-putin-journalists-death-admitted-faked-by-ukraine-as-geopolitical-situation-heats-up.html',
 'https://www.activistpost.com/2018/05/neonatal-hepatitis-b-vaccine-the-autism-influencer-from-day-one-of-life.html',
 'https://www.activistpost.com/2018/05/red-nose-day-recognizes-kids-living-in-poverty-article-the-rich-get-smart-the-poor-get-technology-the-new-digital-divide-in-school-choice-highlights-part-of-the-problem.html',
 'https://www.activistpost.com/2018/05/john-boltons-plan-b-now-operational.html',
 'https://www.activistpost.com/2018/05/former-state-dept-anti-trafficking-chief-admits-efforts-are-overly-focused-on-sex-trafficking.html',
 'https://www.activistpost.com/2018/04/horrifying-testimonies-prove-you-have-been-lied-to-about-eastern-ghouta.html',
 'https://www.activistpost.com/2018/03/april-fools-science-centers-and-and-smart-meters-and-5g-small-cells-and-smokescreens-oh-my.html',
 'https://www.activistpost.com/2018/05/getting-real-about-smart-cities-questions-to-ask-before-your-community-becomes-smart.html',
 'https://www.activistpost.com/2018/06/what-does-epigenetics-mean-for-humanitys-awakening.html',
 'https://www.activistpost.com/2018/05/rand-paul-exposes-congress-plot-to-give-president-unlimited-dictatorial-power-for-war.html',
 'https://www.activistpost.com/2018/05/2005-cnn-host-christiane-amanpour-tells-assad-us-looking-for-new-syrian-leader-supporting-opposition-preparing-coup.html',
 'https://www.activistpost.com/2018/03/how-your-cell-phone-can-make-you-unattractive-and-ruin-your-relationships-acne-impotence-premature-aging-reduced-impulse-control-and-more.html',
 'https://www.activistpost.com/2018/05/social-media-behemoths-sweep-alternative-news-into-the-memory-hole.html',
 'https://www.activistpost.com/2018/03/do-you-love-your-kitty-enough-to-trade-your-smart-phone-for-a-flip-phone-new-study-on-big-cats-explains-why-you-should.html',
 'https://www.activistpost.com/2018/04/canadas-worst-mass-killing-in-30-years-proves-lunatics-who-want-to-kill-people-dont-need-guns.html',
 'https://www.activistpost.com/2018/04/good-drivers-are-creating-a-budget-shortfall-proving-govt-needs-you-to-break-the-law-to-fund-itself.html',
 'https://www.activistpost.com/2018/04/which-state-will-be-the-first-to-suffer-fiscal-collapse.html',
 'https://www.activistpost.com/2018/04/the-dystopian-threat-of-universal-benefits.html',
 'https://www.activistpost.com/2018/04/what-do-cbss60-minutes-dr-oz-the-digital-divide-in-public-schools-and-5g-cell-towers-have-in-common-more-than-you-may-think.html',
 'https://www.activistpost.com/2018/04/how-to-recognize-when-your-society-is-suffering-a-dramatic-decline.html',
 'https://www.activistpost.com/2018/04/cdc-says-over-50-of-ohio-adults-live-in-wireless-only-households-so-lawmakers-pass-hb-478-to-allow-risky-small-cell-tower-installation-everywhere.html',
 'https://www.activistpost.com/2018/04/trump-hands-the-military-industrial-complex-another-massive-win.html',
 'https://www.activistpost.com/2018/05/us-warns-of-firm-response-if-syria-attacks-isis-no-really.html',
 'https://www.activistpost.com/2018/04/is-the-cdc-scheming-for-another-autism-scandal-or-cover-up.html',
 'https://www.activistpost.com/2018/04/the-slippery-slope-to-a-constitution-free-america.html',
 'https://www.activistpost.com/2018/05/is-there-a-cui-bono-already-accruing-from-the-gates-1-15-million-cochrane-group-donation.html',
 'https://www.activistpost.com/2018/04/emmy-winning-journalist-ben-swann-breaks-down-the-situation-in-syria.html',
 'https://www.activistpost.com/2018/04/trump-walks-back-promises-to-declassify-remaining-jfk-files-despite-remaining-questions.html',
 'https://www.activistpost.com/2018/06/forget-agenda-21-uns-2030-agenda-will-transform-the-world.html',
 'https://www.activistpost.com/2018/05/kazakhstan-goes-for-the-gold-again.html',
 'https://www.activistpost.com/2018/05/cdc-study-150-increase-in-autism-in-u-s-kids-since-2000-researchers-suspect-environmental-risks-and-triggers-2012-research-determined-wifi-radiation-disrupts-blood-brain-barrier-may-cause-leaki.html',
 'https://www.activistpost.com/2018/04/examining-the-evidence-for-chemical-attack-in-syria.html',
 'https://www.activistpost.com/2018/04/malaysia-fake-news-bill-imprisonment-journalists-trend.html',
 'https://www.activistpost.com/2018/05/ny-schools-to-install-facial-recognition-tech-used-by-police-and-military.html',
 'https://www.activistpost.com/2018/04/the-least-known-and-best-performing-precious-metal.html',
 'https://www.activistpost.com/2018/05/who-is-buying-votes-at-the-lebanon-election.html',
 'https://www.activistpost.com/2018/06/teacher-posts-2nd-graders-wish-that-cell-phones-didnt-exist-due-to-parents-heavy-use-how-digital-addiction-is-hurting-us-all.html',
 'https://www.activistpost.com/2018/06/why-globalists-want-to-contain-iran.html',
 'https://www.activistpost.com/2018/05/7-countries-in-5-years-2007-wesley-clark-interview-reveals-us-plan-to-go-to-war-with-iraq-iran-syria-libya-lebanon-somalia-and-sudan.html',
 'https://www.activistpost.com/2018/04/why-are-sinclairs-scripted-news-segments-such-a-big-deal.html',
 'https://www.activistpost.com/2018/04/after-mass-shootings-theyre-not-just-coming-for-guns-theyre-coming-for-brains.html',
 'https://www.activistpost.com/2018/05/in-the-wake-of-mass-shootings-parents-reconsider-mass-schooling.html',
 'https://www.activistpost.com/2018/05/slow-motion-genocide-indonesia-is-bombing-west-papua-and-nobodys-talking-about-it.html',
 'https://www.activistpost.com/2018/05/vin-armani-discusses-bitcoin-cash-conference-the-future-of-bitcoin-and-blockchain-governance.html',
 'https://www.activistpost.com/2018/05/an-interview-with-anonymous-on-oprussia-against-the-death-of-anonymity-and-censoring-of-encryption.html',
 'https://www.activistpost.com/2018/04/hard-won-homeschooling-freedoms-are-under-threat-and-must-be-defended.html',
 'https://www.activistpost.com/2018/04/e-waste-recycler-sentenced-to-over-a-year-in-prison-for-fixing-old-pcs-and-selling-them.html',
 'https://www.activistpost.com/2018/05/is-emerging-market-turmoil-deutsche-banks-black-swan.html',
 'https://www.activistpost.com/2018/04/facebook-censorship-the-grotesque-mainstream-solution.html',
 'https://www.activistpost.com/2018/04/wellness-programs-for-seniors-to-include-virtual-reality-when-vr-side-effects-include-balance-issues-behavioral-changes-headaches-and-sore-eyes.html',
 'https://www.activistpost.com/2018/04/5g-wireless-a-ridiculous-front-for-global-control.html',
 'https://www.activistpost.com/2018/05/gold-mining-supply-is-collapsing.html',
 'https://www.activistpost.com/2018/04/its-not-my-fault-my-brain-implant-made-me-do-it.html',
 'https://www.activistpost.com/2018/05/watch-live-meme-orial-day-the-blockchain-wars-with-mance-rayder.html',
 'https://www.activistpost.com/2018/04/appeals-court-rules-nypd-can-hide-surveillance-of-muslims.html',
 'https://www.activistpost.com/2018/04/fake-news-and-the-programmed-viewer.html',
 'https://www.activistpost.com/2018/05/questioning-why-u-s-pregnancy-death-rates-are-so-high.html',
 'https://www.activistpost.com/2018/06/depression-could-cell-phone-and-wifi-radiation-disrupting-the-blood-brain-barrier-be-playing-a-role.html',
 'https://www.activistpost.com/2018/05/hell-hath-no-fury-like-weather-geoengineering.html',
 'https://www.activistpost.com/2018/05/gaza-and-palestine-101-for-americans.html',
 'https://www.activistpost.com/2018/04/19-questions-mark-zuckerberg-strangely-couldnt-answer-during-his-senate-hearing.html',
 'https://www.activistpost.com/2018/03/the-lebanon-israel-border-reasons-for-peace-excuses-for-war.html',
 'https://www.activistpost.com/2018/05/fcc-tired-being-nice-communities-fighting-small-cell-towers.html',
 'https://www.activistpost.com/2018/03/amazon-now-wants-to-photograph-your-home-every-time-they-make-a-delivery.html',
 'https://www.activistpost.com/2018/04/activists-successfully-end-urban-shield-military-police-war-games-training.html',
 'https://www.activistpost.com/2018/05/watch-live-the-vin-armani-show-returns-to-discuss-bitcoins-impact-on-culture.html',
 'https://www.activistpost.com/2018/06/meet-paul-ehrlich-pseudoscience-charlatan.html',
 'https://www.activistpost.com/2018/05/yucky-freedom.html',
 'https://www.activistpost.com/2018/05/activists-uncover-pre-crime-police-program-operated-by-lapd.html',
 'https://www.activistpost.com/2018/04/hey-yo-ohio-your-elected-officials-passed-a-bill-so-telecom-companies-may-now-install-more-small-cell-towers-in-residential-yards-and-everywhere-else.html',
 'https://www.activistpost.com/2018/04/syrian-conflict-is-a-distraction-from-a-secret-war.html',
 'https://www.activistpost.com/2018/05/supreme-court-to-rule-on-your-first-amendment-right-to-silence.html',
 'https://www.activistpost.com/2018/05/u-s-france-setting-the-stage-for-another-false-flag-chem-attack-in-syria-to-justify-more-bombing.html',
 'https://www.activistpost.com/2018/05/ever-wonder-how-wi-fi-routers-create-wi-fi-witness-the-splendor-via-video-demonstrations.html',
 'https://www.activistpost.com/2018/05/new-york-district-attorneys-disobey-immoral-law-now-refusing-to-prosecute-marijuana-arrests.html',
 'https://www.activistpost.com/2018/06/2006-state-department-cable-reveals-plan-to-use-terror-intrigue-kurds-to-destabilize-syria-weaken-assad.html',
 'https://www.activistpost.com/2018/04/shooting-fish-in-a-barrel-world-we-are-all-palestinians-now.html',
 'https://www.activistpost.com/2018/04/respected-businessman-inventor-and-scientist-dr-amar-bose-didnt-want-wireless-antennas-near-homes-or-on-businesses-why-would-you.html',
 'https://www.activistpost.com/2018/06/is-the-next-cryptocurrency-bubble-around-the-corner.html',
 'https://www.activistpost.com/2018/05/missouri-police-using-federal-loophole-to-skim-millions-in-asset-forfeiture-proceeds.html',
 'https://www.activistpost.com/2018/05/ecuadorian-embassy-adds-new-rules-for-julian-assange-no-visitors-phone-calls-or-internet.html',
 'https://www.activistpost.com/2018/05/is-israel-burning.html',
 'https://www.activistpost.com/2018/05/conspiracy-theory-politicians-corporations-admit-to-paying-actors-to-show-fake-support.html',
 'https://www.activistpost.com/2018/04/six-teens-stabbed-during-night-of-violence-in-gun-free-london-mayor-demands-more-knife-control.html',
 'https://www.activistpost.com/2018/04/google-and-kajeet-install-wifi-on-school-buses-when-no-safe-level-of-wifi-has-been-scientifically-determined-for-kids-and-tech-inventors-send-their-kids-to-low-tech.html',
 'https://www.activistpost.com/2018/05/there-are-only-two-ways-this-ends.html',
 'https://www.activistpost.com/2018/04/april-is-autism-awareness-month-2012-research-proved-cell-phone-and-wifi-radiation-disrupts-brain-barrier-causes-it-to-leak-no-safe-level-scientifically-determined-for-kids-or-pregnant-women.html',
 'https://www.activistpost.com/2018/05/us-praises-israeli-restraint-after-it-uses-chemical-weapons-on-civilians-in-gaza.html',
 'https://www.activistpost.com/2018/05/innocent-couple-raided-by-cops-for-facebook-post-of-legal-morel-mushrooms.html',
 'https://www.activistpost.com/2018/04/police-use-fingerprints-pulled-from-whatsapp-photo-to-secure-convictions.html',
 'https://www.activistpost.com/2018/06/facebook-gave-data-access-to-chinese-firm-flagged-by-us-intelligence.html',
 'https://www.activistpost.com/2018/06/schools-replacing-wifi-with-wired-internet-due-to-confirmed-illnesses-and-increased-health-risks-from-exposure-website-provides-locations-and-more.html',
 'https://www.activistpost.com/2018/05/amazons-plan-to-help-police-identify-citizens-in-real-time-and-predict-crimes.html',
 'https://www.activistpost.com/2018/05/is-eugenics-alive-well-and-actually-thriving-today.html',
 'https://www.activistpost.com/2018/04/parallels-between-the-civil-rights-movement-and-denials-of-self-determination-regarding-vaccines.html',
 'https://www.activistpost.com/2018/05/many-u-s-news-stations-are-covering-cell-phone-and-wifi-radiation-concerns-are-yours-saferemr-com-provides-running-list.html',
 'https://www.activistpost.com/2018/04/us-bombs-syria-to-cover-up-lack-of-evidence-on-chem-attacks-discredits-own-claims-by-doing-so.html',
 'https://www.activistpost.com/2018/05/newsweek-is-the-latest-to-warn-about-cell-phone-radiation-wifi-and-5g-technology-causing-harm.html',
 'https://www.activistpost.com/2018/05/windows-not-broken-new-body-cam-of-vegas-shooting-raises-even-more-questions.html',
 'https://www.activistpost.com/2018/05/teen-sent-to-prison-for-defending-home-from-intruders-because-the-intruders-were-cops.html',
 'https://www.activistpost.com/2018/05/33-years-ago-today-police-fire-bombed-a-neighborhood-in-philly-killing-women-and-children.html',
 'https://www.activistpost.com/2018/05/just-like-obama-trumps-warmongering-just-got-him-nominated-for-the-nobel-peace-prize.html',
 'https://www.activistpost.com/2018/05/precedent-set-state-supreme-court-rules-police-cant-arrest-students-for-using-medical-marijuana-on-campus.html',
 'https://www.activistpost.com/2018/05/pentagon-seeks-300-million-in-weapons-for-65000-us-backed-forces-in-syria.html',
 'https://www.activistpost.com/2018/05/dial-t-for-tyranny-while-america-feuds-the-police-state-shifts-into-high-gear.html',
 'https://www.activistpost.com/2018/04/its-spreading-more-anarchists-are-fixing-potholes-because-the-govt-wont-do-its-job.html',
 'https://www.activistpost.com/2018/05/trash-company-owned-by-a-senator-using-cops-to-shake-down-poor-families-unable-to-pay-bills.html',
 'https://www.activistpost.com/2018/04/the-nsa-wants-a-skeleton-key-to-everyones-encrypted-data.html',
 'https://www.activistpost.com/2018/04/good-news-there-are-natural-alternatives-to-treating-opiate-withdrawal-ibogaine-is-one-of-them.html',
 'https://www.activistpost.com/2018/03/911-victims-family-members-lawsuit-against-saudi-arabia-proceed.html',
 'https://www.activistpost.com/2018/04/why-we-have-a-surveillance-state.html',
 'https://www.activistpost.com/2018/05/as-40-of-americans-cant-pay-400-bill-pentagon-spends-1-billion-developing-killer-robots.html',
 'https://www.activistpost.com/2018/04/former-united-nations-climate-expert-calls-for-global-rules-on-geoengineering.html',
 'https://www.activistpost.com/2018/03/why-are-food-water-and-air-lifes-essentials-deliberately-poisoned-part-3-air.html',
 'https://www.activistpost.com/2018/05/inflation-the-peoples-enemy-the-governments-friend.html',
 'https://www.activistpost.com/2018/04/syrian-boy-in-white-helmets-video-reveals-truth-about-alleged-chemical-attack.html',
 'https://www.activistpost.com/2018/04/not-an-april-fools-joke-chinese-space-station-predicted-to-crash-over-earth.html',
 'https://www.activistpost.com/2018/05/rogue-spying-devices-found-in-u-s-states-cause-call-for-concern.html',
 'https://www.activistpost.com/2018/04/tech-moguls-automation-universal-basic-income-doomsday.html',
 'https://www.activistpost.com/2018/05/double-trouble-that-will-do-in-mother-nature-electromagnetic-frequencies-and-glyphosate-if-weather-geoengineering-doesnt-get-us-first.html',
 'https://www.activistpost.com/2018/04/fingerprints-eye-scans-now-required-to-buy-food-in-india-as-banks-cut-off-cryptocurrencies.html',
 'https://www.activistpost.com/2018/04/citing-conclusive-evidence-of-explosives-families-of-victims-file-petition-to-re-open-9-11-investigation.html',
 'https://www.activistpost.com/2018/06/israeli-selling-surveillance-systems-governments-around-world.html',
 'https://www.activistpost.com/2018/04/new-surveillance-camera-software-allows-law-enforcement-to-identify-groups-of-people-in-real-time.html',
 'https://www.activistpost.com/2018/04/finland-ends-its-experiment-with-universal-basic-income.html',
 'https://www.activistpost.com/2018/04/china-takes-the-long-view-on-gold-silver-and-so-should-you.html',
 'https://www.activistpost.com/2018/06/aging-gracefully-challenge-embraced.html',
 'https://www.activistpost.com/2018/04/solutions-spontaneous-order.html',
 'https://www.activistpost.com/2018/04/out-of-top-100-news-outlets-not-a-single-one-questioned-syrian-attack.html',
 'https://www.activistpost.com/2018/05/new-colorado-law-expands-asset-forfeiture-reforms.html',
 'https://www.activistpost.com/2018/05/swamp-drainage-update-ex-fcc-chairman-working-again-for-telecom-industry-and-continuing-to-promote-risky-5g-and-internet-of-things-iot.html',
 'https://www.activistpost.com/2018/04/house-monetary-policy-committee-member-questions-treasury-and-fed-about-their-gold-activities.html',
 'https://www.activistpost.com/2018/05/disruptive-devos-and-the-afc-push-personalized-virtual-school-privatization.html',
 'https://www.activistpost.com/2018/05/as-iran-drops-the-dollar-us-court-orders-them-to-pay-6b-to-victims-of-9-11-despite-no-evidence.html',
 'https://www.activistpost.com/2018/04/florida-activist-who-fought-release-of-gm-mosquitoes-found-dead-in-hotel-pool.html',
 'https://www.activistpost.com/2018/05/they-admitted-social-media-is-programming-us.html',
 'https://www.activistpost.com/2018/05/argentina-is-suddenly-on-the-verge-of-another-economic-collapse.html',
 'https://www.activistpost.com/2018/04/the-war-in-syria-was-a-us-intervention-since-day-1.html',
 'https://www.activistpost.com/2018/05/glyphosate-should-be-banned-by-epa-and-the-law-its-a-hormone-disruptor.html',
 'https://www.activistpost.com/2018/06/5g-mini-cell-towers-junk-yards-on-a-pole-will-affect-your-lifestyle-more-than-you-know.html',
 'https://www.activistpost.com/2018/04/artificial-intelligence-friend-foe-or-another-biblical-tower-of-babel-like-event-in-the-making.html',
 'https://www.activistpost.com/2018/06/5g-woefully-lacking-in-safety-issues-are-fcc-and-icnirp-to-blame.html',
 'https://www.activistpost.com/2018/05/ngos-are-the-deep-states-trojan-horses.html',
 'https://www.activistpost.com/2018/06/if-trump-really-wanted-to-fight-the-deep-state-hed-pardon-these-5-heroes-instead-of-criminals.html',
 'https://www.activistpost.com/2018/05/neocon-john-bolton-tells-a-big-lie-about-iran.html',
 'https://www.activistpost.com/2018/04/us-intervention-in-syria-will-kill-far-more-children-than-assads-alleged-chemical-attack.html',
 'https://www.activistpost.com/2018/04/multiple-cities-come-together-to-pass-ordinances-making-it-illegal-to-ban-guns.html',
 'https://www.activistpost.com/2018/05/emfs-and-rfrs-finally-taken-to-court-in-canada-that-is.html',
 'https://www.activistpost.com/2018/04/interview-with-prepper-we-were-held-without-charges-for-survivalist-facebook-posts.html',
 'https://www.activistpost.com/2018/05/australian-government-press-ignore-hands-off-syria-anti-war-rally-in-melbourne.html',
 'https://www.activistpost.com/2018/05/colorado-smart-pavement-monitor-drivers.html',
 'https://www.activistpost.com/2018/04/deep-state-what-about-elite-television-news-anchors.html',
 'https://www.activistpost.com/2018/05/city-slaps-burn-victim-with-violation-for-not-mowing-lawn-while-he-was-in-the-hospital.html',
 'https://www.activistpost.com/2018/04/facebook-scans-your-photos-and-links-you-send-in-its-messenger-app.html',
 'https://www.activistpost.com/2018/04/bill-maher-on-how-every-generation-could-be-called-the-what-were-you-thinking-generation-cell-phones-in-pockets-included-in-current-list-of-senseless-behavior.html',
 'https://www.activistpost.com/2018/05/the-irony-of-election-fraud-staggering-election-loss-for-the-west-huge-win-for-lebanon.html',
 'https://www.activistpost.com/2018/05/in-2011-the-national-institutes-of-health-nih-acknowledged-cell-phone-radiation-affects-brain-but-wasnt-sure-it-mattered-even-though-earlier-research-said-it-did.html',
 'https://www.activistpost.com/2018/05/us-troops-create-new-military-base-in-syria-despite-turkey-threatening-to-attack.html',
 'https://www.activistpost.com/2018/05/chicago-police-one-step-closer-to-using-drone-surveillance-protests.html',
 'https://www.activistpost.com/2018/04/on-this-day-in-1914-us-military-slaughtered-kids-in-colorado-and-jd-rockefeller-had-media-cover-it-up.html',
 'https://www.activistpost.com/2018/05/jacobson-v-massachusetts-why-it-should-be-scuttled-the-scotus-1905-decision-is-obsolete-and-needs-a-certiorari-brief-filed.html',
 'https://www.activistpost.com/2018/04/police-testing-controversial-portable-dna-machine.html',
 'https://www.activistpost.com/2018/05/russias-relationship-with-israel-and-the-s-300-controversy.html',
 'https://www.activistpost.com/2018/04/doug-casey-on-anarchy-and-voluntaryism.html',
 'https://www.activistpost.com/2018/05/rhode-island-drivers-will-be-fined-100-for-talking-on-cell-phones-starting-june-1st-research-confirmed-cell-phone-radiation-disrupts-blood-brain-barrier-causes-it-to-leak.html',
 'https://www.activistpost.com/2018/04/strike-imminent-trump-threatens-ww3-over-unverified-chemical-weapons-attacks-in-regions-controlled-by-terrorists.html',
 'https://www.activistpost.com/2018/05/trump-administration-obstructing-justice-goldman-sachs-romney-bain-cap.html',
 'https://www.activistpost.com/2018/05/new-assad-interview-syria-will-be-liberated-with-or-without-americans.html',
 'https://www.activistpost.com/2018/04/fake-fake-news-is-a-danger-to-our-fake-democracy.html',
 'https://www.activistpost.com/2018/06/syria-russia-warn-of-potential-chemical-weapons-false-flag-staged-by-us-terrorists.html',
 'https://www.activistpost.com/2018/06/texas-gold-depository-open-for-business.html',
 'https://www.activistpost.com/2018/05/police-use-spying-doorbells-to-create-digital-neighborhood-watch-networks.html',
 'https://www.activistpost.com/2018/04/medela-offers-breastfeeding-advice-through-alexa-alexa-uses-wifi-no-safe-level-of-cell-phone-or-wifi-radiation-scientifically-determined-for-kids-or-pregnant-women.html',
 'https://www.activistpost.com/2018/05/secret-fbi-program-now-jailing-activists-for-speaking-out-against-police-brutality-on-facebook.html',
 'https://www.activistpost.com/2018/04/in-letter-to-ceo-1000s-of-google-employees-revolt-against-military-drone-project.html',
 'https://www.activistpost.com/2018/05/kafkas-nightmare-emerges-chinas-social-credit-score.html',
 'https://www.activistpost.com/2018/04/missouri-action-alert-help-protect-privacy-from-state-federal-surveillance-programs.html',
 'https://www.activistpost.com/2018/05/as-oil-moves-higher-gold-and-gold-stocks-look-better-and-better.html',
 'https://www.activistpost.com/2018/04/social-media-alternatives-yours-org-with-ryan-x-charles.html',
 'https://www.activistpost.com/2018/04/if-you-limit-any-free-speech-this-is-what-you-get.html',
 'https://www.activistpost.com/2018/04/pink-floyd-frontman-leaks-email-exposing-how-white-helmets-recruit-celebs-with-saudi-money.html',
 'https://www.activistpost.com/2018/03/wikileaks-founder-julian-assange-internet-shut-down-again.html',
 'https://www.activistpost.com/2018/05/police-cctv-cameras-turn-citizens-into-stay-at-home-spies-spying-on-their-neighbors-24-7.html',
 'https://www.activistpost.com/2018/04/fake-white-helmets-chemical-attack.html',
 'https://www.activistpost.com/2018/06/council-on-foreign-relations-tells-govt-they-have-to-use-propaganda-on-americans.html',
 'https://www.activistpost.com/2018/04/dhs-wants-to-create-profiles-of-journalists-and-media-influencers-who-mention-its-name.html',
 'https://www.activistpost.com/2018/04/doers-have-the-biggest-impact-on-liberty.html',
 'https://www.activistpost.com/2018/04/how-yulia-and-sergei-skripal-and-their-cat-saved-the-world-a-synopsis-of-the-attack-on-syria.html',
 'https://www.activistpost.com/2018/05/russia-hints-isis-linked-forces-operating-in-us-controlled-zones-in-syria-photos-already-show-us-protecting-terrorists-in-tanf.html',
 'https://www.activistpost.com/2018/05/the-tsa-has-a-new-secret-watch-list-and-you-could-soon-be-added-to-it.html',
 'https://www.activistpost.com/2018/05/ceo-says-wireless-wifi-receiver-mounted-under-bus-is-safe-because-it-doesnt-give-you-any-tingle-or-heat-decades-of-research-says-tingle-or-heat-aren.html',
 'https://www.activistpost.com/2018/05/us-govt-worker-suffers-traumatic-brain-injury-after-abnormal-sound-incident-in-china.html',
 'https://www.activistpost.com/2018/04/we-do-better-than-government-services-with-dan-johnson.html',
 'https://www.activistpost.com/2018/04/epa-faces-lawsuit-for-withholding-records-related-to-pesticide-rule-change.html',
 'https://www.activistpost.com/2018/04/shoot-first-and-think-later-supreme-court-deals-another-blow-to-police-accountability.html',
 'https://www.activistpost.com/2018/04/censorship-is-alive-and-thriving-in-the-usa-especially-via-the-internet.html',
 'https://www.activistpost.com/2018/03/the-florida-school-shooting-survivor-cnn-refused-to-interview.html',
 'https://www.activistpost.com/2018/04/9-11-families-subpoena-fbi-for-documents-related-to-saudi-arabia.html',
 'https://www.activistpost.com/2018/05/the-imfs-reprehensible-campaign-for-continued-poverty-in-sub-saharan-africa.html',
 'https://www.activistpost.com/2018/04/entire-county-refuses-to-obey-new-gun-control-law-declares-itself-gun-owner-sanctuary.html',
 'https://www.activistpost.com/2018/04/environmentalists-who-ignore-electronic-waste-e-waste-are-part-of-the-problem-not-the-solution.html',
 'https://www.activistpost.com/2018/04/gluten-sensitivity-was-ridiculed-until-along-came-celiac-disease-microwave-sickness-or-electrosensitivity-was-discovered-in-the-1950s-and-is-rid.html',
 'https://www.activistpost.com/2018/04/china-moves-to-neuter-king-dollar-in-international-trade.html',
 'https://www.activistpost.com/2018/05/police-cadets-quit-expose-dept-for-training-cops-to-view-public-as-cockroaches-theyre-at-war-with.html',
 'https://www.activistpost.com/2018/06/how-would-you-know-that-youre-safely-using-your-cell-phone-and-other-wifi-devices-if-you-havent-read-the-manuals.html',
 'https://www.activistpost.com/2018/05/the-telegraph-uk-publishes-article-mobile-phone-cancer-warning-as-malignant-brain-tumours-double-duh.html',
 'https://www.activistpost.com/2018/05/trumps-pull-out-nuclear-deal-planned-path-to-persia-war-iran.html',
 'https://www.activistpost.com/2018/04/environmentalists-who-ignore-sources-of-electrical-pollution-electrosmog-are-part-of-the-problem-not-the-solution.html',
 'https://www.activistpost.com/2018/04/astonishing-california-bill-would-shut-down-free-speech-require-fact-checkers.html',
 'https://www.activistpost.com/2018/05/blockchain-patents-corporate-america-youre-doing-it-wrong.html',
 'https://www.activistpost.com/2018/04/mainstream-media-cuts-generals-mic-as-he-tells-the-truth-on-syrian-gas-attack.html',
 'https://www.activistpost.com/2018/05/dont-be-an-idiot-get-rid-of-alexa.html',
 'https://www.activistpost.com/2018/05/us-house-overwhelmingly-passes-717-billion-spending-bill-to-rebuild-our-military.html',
 'https://www.activistpost.com/2018/06/goodbye-monsanto-hello-bayer-on-steroids.html',
 'https://www.activistpost.com/2018/04/army-wants-soldiers-to-3d-print-a-i-robot-squid-in-future-missions.html',
 'https://www.activistpost.com/2018/04/the-fringe-cult-of-peaceful-coexistence.html',
 'https://www.activistpost.com/2018/04/china-begins-monitoring-brain-waves-in-the-workplace-and-military.html',
 'https://www.activistpost.com/2018/04/the-blowback-against-facebook-google-and-amazon-is-just-beginning.html',
 'https://www.activistpost.com/2018/05/how-long-before-police-batmobiles-patrol-our-streets.html',
 'https://www.activistpost.com/2018/04/police-warned-by-family-san-bruno-shooter-would-go-after-youtube-found-her-before-shooting.html',
 'https://www.activistpost.com/2018/04/a-us-ally-is-literally-beheading-people-over-nonviolent-drug-charges.html',
 'https://www.activistpost.com/2018/05/public-to-be-scanned-in-real-time-as-police-body-cameras-may-soon-get-facial-recognition.html',
 'https://www.activistpost.com/2018/05/elon-musk-just-exposed-the-oil-oligarchys-control-over-mainstream-media-in-epic-rant.html',
 'https://www.activistpost.com/2018/04/strikes-on-syria-failed-us-wmd-lies-and-the-israel-approach.html',
 'https://www.activistpost.com/2018/04/police-facial-recognition-dui-kiosks-coming-to-a-city-near-you.html',
 'https://www.activistpost.com/2018/05/citizens-fight-back-as-city-fines-and-arrests-them-for-cracked-driveways-improperly-stacked-firewood.html',
 'https://www.activistpost.com/2018/04/study-links-glyphosate-herbicide-to-shorter-pregnancies.html',
 'https://www.activistpost.com/2018/04/the-problem-with-a-state-cartel-economy-prices-rise-wages-dont.html',
 'https://www.activistpost.com/2018/05/us-military-asking-for-help-locating-explosives-that-fell-off-a-truck-in-north-dakota.html',
 'https://www.activistpost.com/2018/04/social-media-police-intelligence-agencies-collect-biometrics.html',
 'https://www.activistpost.com/2018/05/48-years-ago-today-us-troops-massacred-students-in-ohio-covered-it-up-and-got-away-with-it.html',
 'https://www.activistpost.com/2018/04/pink-floyd-frontman-stops-concert-to-explain-false-flag-chemical-attack-in-syria.html',
 'https://www.activistpost.com/2018/05/cervical-cancer-increases-since-hpv-vaccines-per-swedish-study.html',
 'https://www.activistpost.com/2018/04/national-screen-free-week-starts-april-30-american-academy-of-pediatrics-aap-has-been-concerned-about-rf-exposure-from-cell-phones-and-devices-since-at-least-2012.html',
 'https://www.activistpost.com/2018/04/accidental-foia-reveals-mind-control-documents-heres-further-evidence-this-technology-exists.html',
 'https://www.activistpost.com/2018/04/u-s-govt-exposed-for-conducting-bio-warfare-experiments-in-san-francisco-that-killed-us-citizens.html',
 'https://www.activistpost.com/2018/04/cops-kill-unarmed-dad-in-parking-lot-crash-funeral-to-use-his-dead-finger-to-unlock-phone.html',
 'https://www.activistpost.com/2018/04/smart-meters-and-solar-why-clean-energy-sustainability-conservation-climate-change-mitigation-is-like-a-game-of-whack-a-mole.html',
 'https://www.activistpost.com/2018/04/military-industrial-complex-stocks-sent-crashing-as-north-and-south-korea-achieve-peace.html',
 'https://www.activistpost.com/2018/04/this-week-in-ridiculous-regulations.html',
 'https://www.activistpost.com/2018/06/trump-only-notices-mass-surveillance-when-he-is-the-victim.html',
 'https://www.activistpost.com/2018/04/big-wireless-uses-big-tobacco-tactics-to-divide-and-confuse-us-on-cell-phone-safety-2005-film-thank-you-for-smoking-demonstrates-the-process.html',
 'https://www.activistpost.com/2018/05/another-step-towards-collapse-of-the-petrodollar.html',
 'https://www.activistpost.com/2018/06/mit-creates-serial-killer-a-i-personality-with-reddit-experiment.html',
 'https://www.activistpost.com/2018/04/the-same-govt-that-spies-on-its-citizens-is-lecturing-facebook-ceo-for-same-thing.html',
 'https://www.activistpost.com/2018/05/israel-wont-cooperate-with-un-probe-on-gaza-killings.html',
 'https://www.activistpost.com/2018/05/us-state-passes-law-defining-any-criticism-of-israel-as-anti-semitic-just-as-they-kill-60-civilians.html',
 'https://www.activistpost.com/2018/05/facial-recognition-for-all-international-inbound-and-outbound-passengers-begins-at-orlando-airport-data-retained-for-75-years.html',
 'https://www.activistpost.com/2018/05/facebook-announces-partnership-with-think-tank-connected-to-nato-military-industrial-complex.html',
 'https://www.activistpost.com/2018/04/thousands-of-people-in-only-one-state-have-been-in-jail-for-over-a-year-and-never-proven-guilty.html',
 'https://www.activistpost.com/2018/05/why-having-medical-insurance-is-important-to-everyone-who-loves-you.html',
 'https://www.activistpost.com/2018/05/what-will-happen-to-the-cochrane-groups-sense-of-integrity.html',
 'https://www.activistpost.com/2018/05/google-removes-dont-be-evil-from-its-conduct-as-employees-quit-in-droves-over-project-maven.html',
 'https://www.activistpost.com/2018/04/the-uk-disarmed-its-citizens-murders-now-skyrocketing-as-police-fail-to-protect-defenseless-populace.html',
 'https://www.activistpost.com/2018/04/colombias-murder-rate-is-at-an-all-time-low-but-its-activists-keep-getting-killed.html',
 'https://www.activistpost.com/2018/05/remy-the-longest-time-tsa-version.html',
 'https://www.activistpost.com/2018/05/if-your-cell-phone-and-other-devices-were-making-you-fat-would-you-cut-back-on-using-them-wifi-exposure-causes-blood-sugar-fluctuations-weight-gain-obesity.html',
 'https://www.activistpost.com/2018/05/cognitive-behavioral-workforce-conditioning-through-online-adaptive-learning-technetronics.html',
 'https://www.activistpost.com/2018/06/is-the-planets-hydrologic-cycle-screwed-up-by-weather-geoengineering.html',
 'https://www.activistpost.com/2018/05/activist-holds-up-sign-saying-police-hate-free-speech-so-they-arrest-him-to-prove-him-right.html',
 'https://www.activistpost.com/2018/06/how-savvy-investors-do-and-dont-hedge-against-inflation.html',
 'https://www.activistpost.com/2018/04/reports-claim-syria-russia-capture-british-troops-in-douma-uk-govt-denies.html',
 'https://www.activistpost.com/2018/06/5g-hype-or-horror.html',
 'https://www.activistpost.com/2018/05/do-your-kids-think-wi-fi-is-magic-do-you.html',
 'https://www.activistpost.com/2018/04/cops-running-smog-checkpoints-stopping-motorists-to-check-their-emissions.html',
 'https://www.activistpost.com/2018/04/i-like-energy-efficiency-but-i-dont-want-it-to-give-me-cancer-insomnia-mental-illness-obesity-or-hurt-the-environment-cfl-and-led-light-bulbs-not-so-eco-friendly-after-all.html',
 'https://www.activistpost.com/2018/06/commercial-for-asthma-medication-features-unsafe-use-of-technology-respiratory-health-is-affected-by-cell-phone-and-wifi-radiation-and-electrical-pollution-electrosmog.html',
 'https://www.activistpost.com/2018/04/chemical-weapons-attack-in-syria-an-open-source-investigation.html',
 'https://www.activistpost.com/2018/05/poland-offers-2-billion-for-permanent-us-military-base.html',
 'https://www.activistpost.com/2018/04/a-1991-book-predicted-the-connection-between-mass-shootings-and-public-demand-for-gun-control.html',
 'https://www.activistpost.com/2018/03/sexual-assaults-un-style-go-unresolved-how-come.html',
 'https://www.activistpost.com/2018/04/its-raining-mortars-in-damascus-again-mainstream-media-silent.html',
 'https://www.activistpost.com/2018/04/conspiracy-theory-us-army-has-admitted-to-conducting-100s-of-germ-warfare-tests-on-americans.html',
 'https://www.activistpost.com/2018/04/5-compelling-reasons-why-the-youtube-shooting-has-disappeared-from-headlines.html',
 'https://www.activistpost.com/2018/04/virginia-law-requires-strict-asset-forfeiture-reporting-first-step-toward-reform.html',
 'https://www.activistpost.com/2018/05/the-essential-difference-between-liberty-lovers-and-big-government-types-is-political-tolerance.html',
 'https://www.activistpost.com/2018/05/illinois-police-just-claimed-if-marijuana-is-legalized-theyll-have-to-kill-their-police-dogs.html',
 'https://www.activistpost.com/2018/04/city-of-berkeley-passes-ordinance-taking-on-surveillance-state.html',
 'https://www.activistpost.com/2018/05/city-bans-anarchy-symbol-officials-call-it-hate-speech-similar-to-swastika.html',
 'https://www.activistpost.com/2018/05/jacobson-v-massachusetts-why-it-should-be-scuttled-the-scotus-1905-decision-is-obsolete-and-needs-a-certiorari-brief-filed-part-3-of-3.html',
 'https://www.activistpost.com/2018/05/hypoadrenalism-stress-and-microwaves.html',
 'https://www.activistpost.com/2018/05/cbs-news-is-the-latest-to-report-health-concerns-regarding-5g-small-cell-tower-installation.html',
 'https://www.activistpost.com/2018/05/sacramento-residents-outraged-by-secret-drone-program-spying-neighborhood.html',
 'https://www.activistpost.com/2018/04/2010-nbc-article-1-in-3-are-sensitive-to-wifi-electrical-pollution-electrosmog-and-3-percent-hypersensitive.html',
 'https://www.activistpost.com/2018/04/how-the-globalism-con-game-leads-to-a-new-world-order.html',
 'https://www.activistpost.com/2018/06/unsafe-tech-use-displayed-in-marketing-campaigns-for-prescription-drugs-tv-programs-films-and-more.html',
 'https://www.activistpost.com/2018/05/the-college-scam.html',
 'https://www.activistpost.com/2018/05/good-morning-america-experiment-on-kids-and-unrestricted-screen-time.html',
 'https://www.activistpost.com/2018/05/local-cops-can-skirt-state-limits-on-surveillance-by-joining-federal-task-forces.html',
 'https://www.activistpost.com/2018/05/ai-takes-over-hospital-jobs-in-london-implantable-smart-devices-in-soldiers-and-growing-organs.html',
 'https://www.activistpost.com/2018/04/red-flag-homeland-security-hiring-media-monitoring-services-to-compile-journalist-and-media-influencer-database.html',
 'https://www.activistpost.com/2018/05/can-you-handle-the-truth-lab-testing-can-determine-when-health-woes-are-related-to-cell-phone-radiation-wifi-and-electrical-pollution-electrosmog.html',
 'https://www.activistpost.com/2018/05/family-removes-alexa-devices-after-a-stranger-in-another-town-heard-everything-they-were-saying.html',
 'https://www.activistpost.com/2018/05/dhs-expands-police-spying-by-adding-surveillance-cameras-to-bus-stops.html',
 'https://www.activistpost.com/2018/04/u-s-visa-applicants-could-have-to-disclose-5-years-of-social-media-usage.html',
 'https://www.activistpost.com/2018/04/hero-dad-who-stopped-waffle-house-shooting-raises-nearly-100k-for-victims-in-a-day.html',
 'https://www.activistpost.com/2018/06/dhs-to-give-anti-government-stories-sentiment-ratings.html',
 'https://www.activistpost.com/2018/06/say-what-fcc-chair-ajit-pai-to-congress-no-wireless-exposure-risk-even-though-fdas-25m-study-found-exposure-causes-cancer-5g-cell-tower-installation-continues.html',
 'https://www.activistpost.com/2018/04/syrians-rejoice-as-jaish-al-islam-capitulates-mainstream-media-pushes-chemical-weapons-meme-instead.html',
 'https://www.activistpost.com/2018/04/truth-at-last-the-assassination-of-martin-luther-king.html',
 'https://www.activistpost.com/2018/04/your-genome-may-have-already-been-hacked.html',
 'https://www.activistpost.com/2018/04/high-tech-is-neither-earth-nor-environmentally-friendly.html',
 'https://www.activistpost.com/2018/04/how-gun-control-laws-for-mentally-ill-could-disarm-those-who-question-authority.html',
 'https://www.activistpost.com/2018/05/jacobson-v-massachusetts-why-it-should-be-scuttled-the-scotus-1905-decision-is-obsolete-and-needs-a-certiorari-brief-filed-part-2-of-3.html',
 'https://www.activistpost.com/2018/04/hpv-vaccine-gardasil-kills-confirmed-by-court-ruling.html',
 'https://www.activistpost.com/2018/05/cops-raid-school-hold-teacher-at-gun-point-terrify-kids-to-look-for-an-absent-student.html',
 'https://www.activistpost.com/2018/05/whole-foods-bails-on-gmo-labeling.html',
 'https://www.activistpost.com/2018/05/google-employees-now-quitting-as-company-joins-pentagon-becomes-part-of-the-war-machine.html',
 'https://www.activistpost.com/2018/04/trumps-syria-withdrawal-was-textbook-us-deception.html',
 'https://www.activistpost.com/2018/05/when-43-of-americans-cant-pay-for-food-and-rent-we-can-safely-say-the-economic-collapse-is-here.html',
 'https://www.activistpost.com/2018/04/smart-cities-the-latest-big-tech-boondoggle-includes-health-privacy-and-security-risks-this-aint-rock-n-roll.html',
 'https://www.activistpost.com/2018/05/us-admits-it-lost-1500-immigrant-children-handed-many-of-them-directly-to-human-traffickers.html',
 'https://www.activistpost.com/2018/05/25-of-americans-suffer-when-exposed-to-common-chemicals-adding-wifi-radiation-and-electromagnetic-fields-emfs-bigger-toxic-nightmare.html',
 'https://www.activistpost.com/2018/05/the-most-important-election-in-the-world-lebanon-what-election.html',
 'https://www.activistpost.com/2018/05/if-any-other-country-was-shooting-civilians-like-israel-the-us-invasion.html',
 'https://www.activistpost.com/2018/04/a-whistleblower-blows-the-lid-off-microwave-towers.html',
 'https://www.activistpost.com/2018/05/independent-uk-covers-skull-and-bones-leaves-out-key-facts.html',
 'https://www.activistpost.com/2018/06/eye-in-the-sky-drone-surveillance-detect-violence.html',
 'https://www.activistpost.com/2018/06/the-even-older-plan-for-world-government-youve-never-heard-of.html',
 'https://www.activistpost.com/2018/04/dying-to-be-thin-you-may-be-psyched-that-research-claims-exposure-to-5g-cell-towers-could-increase-your-metabolism-but-what-will-it-do-to-your-kids-and-pets.html',
 'https://www.activistpost.com/2018/05/do-you-have-respiratory-issues-exposure-to-cell-phone-radiation-dirty-electricity-wifi-and-other-sources-of-electrosmog-can-make-it-worse.html',
 'https://www.activistpost.com/2018/04/the-truth-about-the-syria-chemical-attacks-no-evidence-of-assad-chem-weapons-western-false-flag-seems-likely.html',
 'https://www.activistpost.com/2018/03/retroactive-racketeering-romney-kills-toys-r-us.html',
 'https://www.activistpost.com/2018/05/trump-sidekick-giuliani-addresses-terror-group-convention.html',
 'https://www.activistpost.com/2018/05/samsung-5g-home-router-wins-fcc-approval-ahead-of-verizons-2018-launch-now-verizon-should-stop-installing-risky-5g-small-cell-towers-in-front-of-homes-and-everywhere-else-but-they-won.html',
 'https://www.activistpost.com/2018/05/businesses-will-use-facial-biometrics-to-create-their-own-watch-lists.html',
 'https://www.activistpost.com/2018/04/the-right-to-bear-arms.html']

def get_article(url):
#Sends request for url
    html = requests.get(url).text
    return html

def parse_article(html):
#BeautifulSoups the article
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h1', class_='entry-title').text
    body = soup.find('div', class_='entry-content clearfix').text

    article = {
        'title': title,
        'body': body,
        'source': 'Activist Post',
        'num_source': 15
    }

    return article

def get_parsed_article_from_link(url):
#Runs the previous two functions on the url
    return parse_article(get_article(url))
#phase 1: uses request to try to BeautifulSoup links
actpost_list_o_articles = []
actpost_problem_articles = []
for text in actpost_first_articles:
    #print(text)
    try:
        art = get_parsed_article_from_link(text.encode())
        actpost_list_o_articles.append(art)

    except:
        #print("Problem processing url " + text)
        problem = text
        actpost_problem_articles.append(problem)
    time.sleep(2)
#phase 2: uses selenium to go through links
driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
for x in actpost_problem_articles:
    try:
        driver.get(x)
        time.sleep(3)
        soupy = BeautifulSoup(driver.page_source, 'lxml')
        title = soupy.find('h1', class_='article-header__title').text
        body = soupy.find('div', class_='entry-content clearfix').text

        articley = {
        'title': title,
        'body': body,
        'source': 'Activist Post',
        'num_source': 15
        }
        actpost_list_o_articles.append(articley)
    except:
        pass
#phase 1: uses request to try to BeautifulSoup links
actpost_more_list_o_articles = []
actpost_more_problem_articles = []
for text in actpost_more_articles:
    #print(text)
    try:
        art = get_parsed_article_from_link(text.encode())
        actpost_more_list_o_articles.append(art)

    except:
        #print("Problem processing url " + text)
        problem = text
        actpost_problem_articles.append(problem)
    time.sleep(2)
#phase 2: uses selenium to go through links
driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
for x in actpost_more_problem_articles:
    try:
        driver.get(x)
        time.sleep(3)
        soupy = BeautifulSoup(driver.page_source, 'lxml')
        title = soupy.find('h1', class_='article-header__title').text
        body = soupy.find('div', class_='entry-content clearfix').text

        articley = {
        'title': title,
        'body': body,
        'source': 'Activist Post',
        'num_source': 15
        }
        actpost_more_list_o_articles.append(articley)
    except:
        pass
all_articles = actpost_list_o_articles + actpost_more_list_o_articles

#starts client in Mongodb
client = MongoClient()
biased_news = client.project5.biased_news
#creates event and loads articles into Mongodb
db = client.events
biased_news = db.biased_news
biased_news.insert_many(all_articles)
