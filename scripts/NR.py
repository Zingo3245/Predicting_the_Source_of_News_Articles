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

NR_links = (
['https://www.nationalreview.com/corner/mccarthy-report-introduction/',
'https://www.nationalreview.com/bench-memos/a-look-at-president-trumps-15th-wave-of-judicial-nominees/',
'https://www.nationalreview.com/news/police-confiscate-ar-15-and-ammo-from-potential-ohio-school-shooter/',
'https://www.nationalreview.com/bench-memos/who-is-eric-murphy/',
'https://www.nationalreview.com/photos/fuego-volcano-guatemala-eruptions/',
'https://www.nationalreview.com/2018/06/donald-trumps-trade-war-sparks-congressional-backlash/',
'https://www.nationalreview.com/photos/recreating-napoleon-invasion-of-malta-1798/',
'https://www.nationalreview.com/news/robert-mueller-files-superseding-indictment-against-paul-manafort/',
'https://www.nationalreview.com/news/robert-mueller-probe-legitimate-say-pluarilty-voters/',
'https://www.nationalreview.com/corner/more-twisted-logic-on-obamacare/',
'https://www.nationalreview.com/photos/top-shots-week-june-2018/',
'https://www.nationalreview.com/2018/06/trump-administration-norms-values-need-evaluation/',
'https://www.nationalreview.com/2018/06/objectivity-among-white-mythologies/'])

more_NR_links = (
['https://www.nationalreview.com/news/dscc-chairman-welcomes-clintons-involvement-in-midterms/',
'https://www.nationalreview.com/2018/06/bill-clinton-me-too-sexual-harassment-democrats-abandon/',
'https://www.nationalreview.com/bench-memos/this-day-in-liberal-judicial-activism-may-30/',
'https://www.nationalreview.com/2018/05/north-korea-summit-cancelled-good-riddance/',
'https://www.nationalreview.com/news/joy-reid-apologizes-after-more-offensive-blog-posts-surface/',
'https://www.nationalreview.com/2018/06/president-trump-not-destroying-himself/',
'https://www.nationalreview.com/2018/06/immigration-debate-immigrants-not-disproportionately-criminal/',
'https://www.nationalreview.com/news/bipartisan-dodd-frank-reform-bill-moves-to-trumps-desk/',
'https://www.nationalreview.com/news/vladimir-putin-syria-russian-troops-staying-indefinitely/',
'https://www.nationalreview.com/2018/06/donald-trump-superlative-job-report-economy-roaring/',
'https://www.nationalreview.com/2018/05/obama-administration-politicized-intelligence-law-enforcement-apparatus/',
'https://www.nationalreview.com/corner/jeff-sessions-gun-law-enforcement-more-than-thoughts-and-prayers/',
'https://www.nationalreview.com/corner/masterpiece-cakeshop-already-protecting-religious-liberty/',
'https://www.nationalreview.com/news/fusion-gps-testimony-extremely-misleading-chuck-grassley/',
'https://www.nationalreview.com/bench-memos/in-god-we-trust-constitutional-sixth-circuit/',
'https://www.nationalreview.com/news/texas-governor-cancels-shotgun-giveaway-plan-after-school-shooting/',
'https://www.nationalreview.com/2018/05/trump-steel-tariffs-undermine-national-security/',
'https://www.nationalreview.com/corner/tucker-carlson-college-cost-coverage-new-education-attitude/',
'https://www.nationalreview.com/2018/05/donald-trump-outsider-president-bureaucrats-run-government/',
'https://www.nationalreview.com/corner/a-right-to-life-for-fungi-but-not-unborn-humans/',
'https://www.nationalreview.com/2018/06/donald-trumps-trade-war-sparks-congressional-backlash/',
'https://www.nationalreview.com/corner/donald-trump-joseph-mccarthy-similarities-differences/',
'https://www.nationalreview.com/bench-memos/judicial-nominations-update-19/',
'https://www.nationalreview.com/corner/president-trump-views-on-same-sex-marriage/',
'https://www.nationalreview.com/2018/06/president-donald-trump-obstruction-argument-lawyers-move-goalposts/',
'https://www.nationalreview.com/news/russian-foreign-minister-will-visit-north-korea-for-talks/',
'https://www.nationalreview.com/corner/donald-trumps-coal-plan-is-bad-news/',
'https://www.nationalreview.com/2018/05/tight-labor-market-good-for-american-workers-best-social-policy/',
'https://www.nationalreview.com/news/trump-unconstitutional-mueller-appointment-tweet/',
'https://www.nationalreview.com/bench-memos/twitter-first-amendment-trump-blocking-ruling/',
'https://www.nationalreview.com/2018/05/initiative-77-bad-deal-for-restaurant-servers/',
'https://www.nationalreview.com/2018/06/obama-administration-iran-deal-failure-and-reckoning/',
'https://www.nationalreview.com/news/pompeo-dines-with-top-north-korean-official-in-new-york/',
'https://www.nationalreview.com/bench-memos/who-is-jonathan-kobes/',
'https://www.nationalreview.com/2018/05/roseanne-barr-firing-justified-not-free-speech-issue/',
'https://www.nationalreview.com/2018/05/conservatives-must-argue-about-ideas-not-trump/',
'https://www.nationalreview.com/news/andrew-cuomo-pens-open-letter-to-trump-after-school-shooting/',
'https://www.nationalreview.com/news/north-korea-summit-trump-withdraws-kim-jong-un-meeting/',
'https://www.nationalreview.com/corner/koch-brothers-trump-free-trade-push-target-policies/',
'https://www.nationalreview.com/2018/05/california-sexual-orientation-bill-would-censor-religious-viewpoints/',
'https://www.nationalreview.com/2018/06/title-x-new-rule-requires-planned-parenthood-to-report-sexual-abuse/',
'https://www.nationalreview.com/news/steve-scalise-returns-to-congressional-baseball-practice-one-year-after-shooting/',
'https://www.nationalreview.com/2018/05/pro-life-churches-must-help-foster-parents/',
'https://www.nationalreview.com/corner/court-ruling-trump-cannot-block-twitter-users-mistaken/',
'https://www.nationalreview.com/2018/05/ireland-abortion-referendum-new-legal-regime-proposal/',
'https://www.nationalreview.com/news/obama-administration-secretly-helped-iran-skirt-financial-sanctions/',
'https://www.nationalreview.com/2018/05/donald-trump-danger-us-democracy/',
'https://www.nationalreview.com/news/north-korea-war-with-us-trump-ready-if-necessary/',
'https://www.nationalreview.com/2018/05/bill-kristol-republicans-should-challenge-trump-in-2020-primaries/',
'https://www.nationalreview.com/2018/05/russia-investigation-clinton-pollster-mark-penn-opposes/',
'https://www.nationalreview.com/news/starbucks-executive-chairman-howard-schultz-stepping-down/',
'https://www.nationalreview.com/news/steve-bannon-admits-defeat-in-campaign-to-oust-gop-incumbents/',
'https://www.nationalreview.com/2018/05/trump-kim-singapore-summit-world-best-interest/',
'https://www.nationalreview.com/news/russia-investigation-doj-providing-congress-new-information/',
'https://www.nationalreview.com/news/trump-kim-summit-singapore-back-on-june-12/',
'https://www.nationalreview.com/2018/05/university-of-michigan-speech-lawsuit-could-end-suppression-culture/',
'https://www.nationalreview.com/2018/05/abortion-politics-of-mayor-stops-womens-care-center-south-bend/',
'https://www.nationalreview.com/2018/06/google-defense-department-pullout-dont-fight-evil/',
'https://www.nationalreview.com/bench-memos/this-day-in-liberal-judicial-activism-may-20/',
'https://www.nationalreview.com/corner/greenhouse-misleads-on-title-x/',
'https://www.nationalreview.com/news/mike-pence-kim-could-end-up-like-qaddafi/',
'https://www.nationalreview.com/news/north-korea-summit-poll-72-percent-approve-trump/',
'https://www.nationalreview.com/news/trump-north-korea-talks-ongoing-kim-meeting-possible/',
'https://www.nationalreview.com/2018/05/north-korean-negotiations-success-is-possible/',
'https://www.nationalreview.com/corner/hhs-lost-kids-statement/',
'https://www.nationalreview.com/news/jobs-report-may-unemployment-18-year-low/',
'https://www.nationalreview.com/2018/06/andrew-mccabe-seeks-immunity-judiciary-committee/',
'https://www.nationalreview.com/2018/06/masterpiece-cakeshop-ruling-religious-liberty-victory/',
'https://www.nationalreview.com/2018/05/eric-greitens-missouri-republicans-accountable/',
'https://www.nationalreview.com/bench-memos/this-day-in-liberal-judicial-activism-may-22/',
'https://www.nationalreview.com/corner/john-brennan-dishonesty-long-record/',
'https://www.nationalreview.com/2018/06/teacher-pay-inefficient-not-too-low-correct-structural-issues/',
'https://www.nationalreview.com/2018/06/donald-trump-can-president-pardon-himself-complicated-question/',
'https://www.nationalreview.com/corner/law-school-declining-enrollment-three-ways-change/',
'https://www.nationalreview.com/magazine/2018/06/11/negan-walking-dead-authoritarianism-like-china/',
'https://www.nationalreview.com/corner/heres-a-college-that-says-yes-to-latin-no-to-federal-money/',
'https://www.nationalreview.com/2018/06/president-trump-strengthening-constitutional-checks-and-balances/',
'https://www.nationalreview.com/corner/swedens-elections-2018-immigration-drives-center-left-voters-away/',
'https://www.nationalreview.com/magazine/2018/06/25/under-fire/',
'https://www.nationalreview.com/news/mike-pompeo-says-kim-jong-un-assured-he-is-ready-to-denuclearize/',
'https://www.nationalreview.com/the-morning-jolt/bill-clinton-metoo-defense-monica-lewinsky-excuses/',
'https://www.nationalreview.com/2018/05/social-security-warning-future-benefits-bold-leadership-needed/',
'https://www.nationalreview.com/corner/donald-trump-department-of-justice-scandal/',
'https://www.nationalreview.com/bench-memos/who-is-chad-readler/',
'https://www.nationalreview.com/corner/school-shootings-national-crisis/',
'https://www.nationalreview.com/2018/05/us-criminal-justice-overhaul-overdue/',
'https://www.nationalreview.com/2018/05/immigration-policy-debate-good-arguments-on-all-sides/',
'https://www.nationalreview.com/bench-memos/this-day-in-liberal-judicial-activism-june-1/',
'https://www.nationalreview.com/2018/05/second-amendment-slavery-nyt-piece-misleading-claims/',
'https://www.nationalreview.com/news/united-kingdom-northern-ireland-abortion-ban/',
'https://www.nationalreview.com/corner/dinesh-dsouza-pardon-just/',
'https://www.nationalreview.com/corner/ireland-abortion-referendum-rejects-catholic-church-and-liberalism/',
'https://www.nationalreview.com/corner/daca-deal-republicans-offer-wall-legalization/',
'https://www.nationalreview.com/2018/06/ireland-abortion-referendum-irish-exceptionalism-ending-european-identity/',
'https://www.nationalreview.com/the-morning-jolt/midterm-elections-2018-polls-good-republicans/',
'https://www.nationalreview.com/corner/gun-politics-do-polls-show-a-change/',
'https://www.nationalreview.com/news/ireland-abortion-referendum-vote/',
'https://www.nationalreview.com/2018/06/supreme-court-masterpiece-cakeshop-ruling-affirms-tolerance-first-amendment/',
'https://www.nationalreview.com/2018/05/foster-care-how-to-improve-and-promote/',
'https://www.nationalreview.com/news/wilbur-ross-commerce-department-has-reached-a-deal-with-sanctioned-chinese-telecom-giant/',
'https://www.nationalreview.com/2018/06/mass-public-shooters-shouldnt-be-named-media/',
'https://www.nationalreview.com/news/paul-ryan-spygate-trey-gowdy-right/',
'https://www.nationalreview.com/corner/fbi-agent-accidental-discharge-gun-colorado-bar-may-face-consequences/',
'https://www.nationalreview.com/2018/05/catholic-social-services-lawsuit-over-foster-care-in-philadelphia/',
'https://www.nationalreview.com/news/north-korean-nuclearizaton-must-happen-deal-trump/',
'https://www.nationalreview.com/2018/06/donald-trump-joseph-mccarthy-comparison-bogus/',
'https://www.nationalreview.com/2018/05/marijuana-like-big-tobacco-predatory-industry/',
'https://www.nationalreview.com/bench-memos/flipping-judicial-seats/',
'https://www.nationalreview.com/news/trump-to-skip-g7-climate-session-after-twitter-fight-with-trudeau-macron/',
'https://www.nationalreview.com/news/jobs-report-gap-between-black-and-white-unemployment-hits-record-low/',
'https://www.nationalreview.com/news/trey-gowdy-defends-fbi-probe-of-trump-campaign/',
'https://www.nationalreview.com/corner/north-korea-trump-summit-cancelling-right-move/',
'https://www.nationalreview.com/news/joy-reid-john-mccain-photoshop-blog-post/',
'https://www.nationalreview.com/news/rubio-trump-administration-surrendered-to-china/',
'https://www.nationalreview.com/2018/06/united-states-needs-space-force-national-security-interest/',
'https://www.nationalreview.com/corner/ed-gillespie-joins-americas-kids-belong-focused-on-foster-care/',
'https://www.nationalreview.com/news/doj-seized-times-reporters-communications-in-leaks-probe/',
'https://www.nationalreview.com/news/trump-north-korea-summit-kim-could-still-happen/',
'https://www.nationalreview.com/2018/06/trump-lawyers-mueller-letter-two-things-right/',
'https://www.nationalreview.com/bench-memos/trump-twitter-first-amendment/',
'https://www.nationalreview.com/2018/05/ms-13-trump-democrats-play-republicans-hand/',
'https://www.nationalreview.com/bench-memos/judicial-nominations-update-20/',
'https://www.nationalreview.com/news/joy-reid-blog-post-attacked-wolf-blitzer-for-being-too-soft-on-jews/',
'https://www.nationalreview.com/news/obama-netflix-deal-barack-michelle-multi-year-agreement/',
'https://www.nationalreview.com/news/devin-nunes-russia-investigation-doj-documents/',
'https://www.nationalreview.com/news/naral-launches-campaign-to-ensure-democrats-win-house-majority/',
'https://www.nationalreview.com/2018/05/corey-robin-book-reactionary-mind-caricature-of-conservatism/',
'https://www.nationalreview.com/corner/midterm-elections-polls-generic-ballot-enthusiasm-gap/',
'https://www.nationalreview.com/2018/06/masterpiece-cakeshop-scotus-decision-broad-enough/',
'https://www.nationalreview.com/corner/migrant-children-lost-federal-agents/',
'https://www.nationalreview.com/2018/05/starbucks-bathroom-policy-terrible-idea/',
'https://www.nationalreview.com/news/trump-campaign-fbi-spying-doj-calls-for-probe/',
'https://www.nationalreview.com/2018/06/masterpiece-cakeshop-case-supreme-court-slaps-down-bias-police/',
'https://www.nationalreview.com/corner/study-clocks-economic-growth-productivity-work-culture/',
'https://www.nationalreview.com/2018/05/trump-russia-investigation-obama-administration-spying-hypocritical/',
'https://www.nationalreview.com/2018/05/department-of-justice-probe-of-fbi-trump-investigation-warranted/',
'https://www.nationalreview.com/bench-memos/this-day-in-liberal-judicial-activism-may-29/',
'https://www.nationalreview.com/2018/06/donald-trump-steel-tariff-senseless/',
'https://www.nationalreview.com/2018/06/obama-trump-administrations-elites-value-style-over-substance/',
'https://www.nationalreview.com/2018/06/china-bullies-foreign-companies-into-espousing-its-worldview/',
'https://www.nationalreview.com/corner/ireland-abortion-referendum-polls-show-ambivalent-voters/',
'https://www.nationalreview.com/corner/trade-and-protection-the-unending-struggle/',
'https://www.nationalreview.com/news/greg-abbott-gun-control-group-blames-texas-governor-shooting/',
'https://www.nationalreview.com/news/hhs-reports-of-1475-lost-unaccompanied-minors-completely-false/',
'https://www.nationalreview.com/2018/05/bob-menendez-problem-for-new-jersey-democrats-midterms/',
'https://www.nationalreview.com/news/pope-francis-climate-change-oil-executives-meeting/',
'https://www.nationalreview.com/2018/05/scandal-politics-temptation-left-has-given-in-utterly/',
'https://www.nationalreview.com/2018/05/jon-favreau-twitter-fail-obama-media-narratives/',
'https://www.nationalreview.com/corner/federal-reserve-interest-rates/',
'https://www.nationalreview.com/corner/universal-background-checks-increase-homicide/',
'https://www.nationalreview.com/corner/china-trade-war-trump-may-declare-victory-stop/',
'https://www.nationalreview.com/2018/06/international-human-rights-community-freedom-often-must-yield/',
'https://www.nationalreview.com/2018/05/trump-russia-investigation-separating-conspiracy-from-reality/',
'https://www.nationalreview.com/2018/06/deep-state-debate-like-mccarthy-era-but-no-communist-threat/',
'https://www.nationalreview.com/2018/05/american-educated-elite-not-educated-not-elite/',
'https://www.nationalreview.com/2018/05/trump-campaign-spying-obama-administration-investigation/',
'https://www.nationalreview.com/news/masterpiece-cakeshop-religious-liberty-wins-landslide/',
'https://www.nationalreview.com/bench-memos/republicans-stacking-courts-democrats-claims-false/',
'https://www.nationalreview.com/news/jeff-sessions-trump-wishes-picked-different-attorney-general/',
'https://www.nationalreview.com/corner/dollar-reserve-currency-status-downside/',
'https://www.nationalreview.com/2018/05/clinton-email-trump-russia-probes-justice-department-double-standards/',
'https://www.nationalreview.com/corner/daca-dreamers-congress-immigration-divisions-deal-unlikely/',
'https://www.nationalreview.com/bench-memos/who-is-eric-murphy/',
'https://www.nationalreview.com/news/freedom-caucus-joins-democrats-tank-farm-bill/',
'https://www.nationalreview.com/2018/05/the-great-revolt-book-reveals-roots-of-trumpism-working-class-support/',
'https://www.nationalreview.com/news/robert-mueller-files-superseding-indictment-against-paul-manafort/',
'https://www.nationalreview.com/news/chelsea-clinton-defends-ivanka-trump-against-vulgar-comments/',
'https://www.nationalreview.com/bench-memos/this-day-in-liberal-judicial-activism-may-24/',
'https://www.nationalreview.com/corner/the-letter-from-trumps-lawyers/',
'https://www.nationalreview.com/news/charles-krauthammer-announces-he-has-weeks-to-live/',
'https://www.nationalreview.com/2018/06/state-constitutions-important-components-of-federalism/',
'https://www.nationalreview.com/2018/05/ireland-abortion-referendum-human-rights-unborn/',
'https://www.nationalreview.com/2018/06/donald-trump-pardons-hypocritical-criticism-by-democrats-media/',
'https://www.nationalreview.com/bench-memos/trump-twitter-ruling-first-amendment-argument-wrong/',
'https://www.nationalreview.com/2018/06/democrats-might-ruin-their-midterm-chances-jobs-economy-strong/',
'https://www.nationalreview.com/news/marijuana-legislation-protect-states-legalize/',
'https://www.nationalreview.com/2018/06/liberal-complaints-about-higher-gas-prices-hypocritical/',
'https://www.nationalreview.com/corner/higher-education-reform-bill-can-congress-pass/',
'https://www.nationalreview.com/bench-memos/improving-the-ninth-circuit/',
'https://www.nationalreview.com/sponsored?prx_t=8qIDAfuYgA3JkQA&amp;&amp;ntv_gscat=19&amp;ntv_fr',
'https://www.nationalreview.com/news/broward-sheriffs-office-denied-paramedics-entry-parkland-school/',
'https://www.nationalreview.com/2018/05/president-taft-resisted-progressive-populism/',
'https://www.nationalreview.com/2018/06/new-york-lawsuit-against-nra-sets-dangerous-precedent/',
'https://www.nationalreview.com/news/trump-administration-explores-auto-tariffs-citing-national-security-concerns/',
'https://www.nationalreview.com/news/professor-convicted-after-spraying-nra-lobbyists-home-with-fake-blood/',
'https://www.nationalreview.com/corner/colleges-teach-writing-poorly-how-to-change/',
'https://www.nationalreview.com/corner/fuel-standards-cafe-epa-rolls-back/',
'https://www.nationalreview.com/2018/06/president-trump-right-to-commute-alice-johnson-sentence/',
'https://www.nationalreview.com/2018/05/foster-care-should-be-national-priority/',
'https://www.nationalreview.com/news/kim-kardashian-trump-meeting-prison-reform-white-house/',
'https://www.nationalreview.com/news/michael-avenatti-withdraws-from-cohen-case-after-judge-orders-halt-to-publicity-tour/',
'https://www.nationalreview.com/news/iran-american-leaders-will-die-like-saddam-if-they-attack/',
'https://www.nationalreview.com/bench-memos/this-day-in-liberal-judicial-activism-may-27/',
'https://www.nationalreview.com/2018/05/farm-bill-let-it-stay-dead-welfare-for-farmers-destructive/',
'https://www.nationalreview.com/2018/05/trump-animals-comment-ms-13-why-it-offends-left/',
'https://www.nationalreview.com/bench-memos/this-day-in-liberal-judicial-activism-may-31/',
'https://www.nationalreview.com/bench-memos/this-day-in-liberal-judicial-activism-may-28/',
'https://www.nationalreview.com/news/russian-journalist-critical-of-putin-shot-dead-in-ukraine/',
'https://www.nationalreview.com/2018/06/wisconsin-case-separation-of-powers-leave-judging-to-judges/',
'https://www.nationalreview.com/news/robert-mueller-probe-legitimate-say-pluarilty-voters/',
'https://www.nationalreview.com/2018/06/masterpiece-cakeshop-ruling-win-for-religious-freedom/',
'https://www.nationalreview.com/corner/the-downsides-of-right-to-try/',
'https://www.nationalreview.com/news/ted-cruz-leads-beto-orourke-hispanics-poll/',
'https://www.nationalreview.com/news/israel-icc-palestinians-demand-criminal-investigation/',
'https://www.nationalreview.com/corner/trey-gowdy-trump-fbi-comments-voice-of-reason/',
'https://www.nationalreview.com/corner/too-many-asian-americans/',
'https://www.nationalreview.com/bench-memos/this-day-in-liberal-judicial-activism-june-7/',
'https://www.nationalreview.com/2018/05/gerrymandering-examples-caused-liberal-judges/',
'https://www.nationalreview.com/news/usa-today-stands-by-lost-immigrant-kids-piece-despite-backlash/',
'https://www.nationalreview.com/2018/05/bank-discriminating-against-guns-free-market/',
'https://www.nationalreview.com/news/mike-pompeo-iran-strongest-sanctions-us-history-coming/',
'https://www.nationalreview.com/news/august-recess-senate-mcconnell-cancels/',
'https://www.nationalreview.com/corner/trumps-retreat-on-china-is-on-balance-welcome/',
'https://www.nationalreview.com/corner/fred-fleitz-not-a-neo-nazi/',
'https://www.nationalreview.com/corner/trump-administration-title-x-policy-jill-filipovic-comments/',
'https://www.nationalreview.com/2018/05/mitch-mcconnell-wins-long-game-for-conservatives/',
'https://www.nationalreview.com/news/rudy-giuliani-north-korea-kim-begged-trump-summit/',
'https://www.nationalreview.com/news/california-democrats-survive-primaries-avoid-being-shut-out-key-races/',
'https://www.nationalreview.com/news/paul-manafort-judge-suppress-fbi-evidence/',
'https://www.nationalreview.com/corner/getting-the-abortion-funding-story-wrong/',
'https://www.nationalreview.com/bench-memos/democrats-beyond-bounds-demagoguery/',
'https://www.nationalreview.com/news/midterm-elections-polls-republicans-take-lead-democrats/',
'https://www.nationalreview.com/photos/top-shots-week-june-2018/',
'https://www.nationalreview.com/corner/planned-parenthood-trump-cuts-funding-good-pro-life-step/',
'https://www.nationalreview.com/corner/masterpiece-cakeshop-decision-against-the-killjoys/',
'https://www.nationalreview.com/2018/06/prison-reform-bill-first-step-act-senate-may-not-hold-vote/',
'https://www.nationalreview.com/bench-memos/this-day-in-liberal-judicial-activism-may-23/',
'https://www.nationalreview.com/2018/06/faith-ryan-whittlesey-reagan-diplomat-remarkable-conservative/',
'https://www.nationalreview.com/news/saudi-arabia-women-drivers-license/',
'https://www.nationalreview.com/corner/affirmative-action-asian-americans-bill-de-blasio-edition/',
'https://www.nationalreview.com/2018/06/sirhan-sirhan-forgotten-terrorist-assassination-of-robert-kennedy/',
'https://www.nationalreview.com/2018/06/firing-line-pbs-revives-needed-institution-margaret-hoover-host/',
'https://www.nationalreview.com/2018/05/mueller-investigation-double-standard-democrats-media/',
'https://www.nationalreview.com/news/mueller-accuses-manafort-of-witness-tampering-asks-judge-to-revoke-his-release/',
'https://www.nationalreview.com/2018/05/trump-china-deal-wont-help-economy/',
'https://www.nationalreview.com/bench-memos/big-victory-for-doj-in-alien-minor-abortion-case/',
'https://www.nationalreview.com/corner/free-speech-college-campuses-taking-beating/',
'https://www.nationalreview.com/2018/06/roseanne-barr-samantha-bee-neither-deserve-firing-for-offensive-speech/',
'https://www.nationalreview.com/2018/05/foster-care-pope-francis-encourages-caring-for-vulnerable/',
'https://www.nationalreview.com/corner/obamacare-lawsuits-absurdity/',
"https://www.nationalreview.com/sponsored?prx_t=8qIDAfuYgA3JkQA&amp;&amp;ntv_gscat=19', true, this, '1087964-238322');",
'https://www.nationalreview.com/2018/05/gop-mideterm-2018-election-prospects-positive/',
'https://www.nationalreview.com/news/supreme-court-abortion-immigration-case-rejects-lower-court-ruling/',
'https://www.nationalreview.com/corner/masterpiece-cakeshop-decision-medical-conscience-rights/',
'https://www.nationalreview.com/2018/06/matthew-charles-deserves-pardon-turned-his-life-around/',
'https://www.nationalreview.com/corner/donald-trump-animals-comment/',
'https://www.nationalreview.com/2018/06/second-amendment-gun-rights-congress-must-act-to-enforce/',
'https://www.nationalreview.com/2018/05/seattle-employee-tax-will-drive-out-corporations-not-homeless/',
'https://www.nationalreview.com/corner/chimpanzee-personhood-supported-new-york-judge/',
'https://www.nationalreview.com/news/paul-ryan-tells-house-gop-act-like-a-majority/',
'https://www.nationalreview.com/2018/06/ronald-mortensen-trump-nominee-dishonest-smear-campaign/',
'https://www.nationalreview.com/2018/06/trump-administration-norms-values-need-evaluation/',
'https://www.nationalreview.com/news/ig-report-comey-defied-authority-fbi-director/',
'https://www.nationalreview.com/2018/06/masterpiece-cakeshop-setback-liberty/',
'https://www.nationalreview.com/2018/06/book-review-the-world-as-it-is-ben-rhodes-obama-reaction-trump-election/',
'https://www.nationalreview.com/news/house-passes-right-to-try-bill-for-terminally-ill-patients/',
'https://www.nationalreview.com/2018/05/trump-trade-policy-on-china-not-about-enforcing-rules/',
'https://www.nationalreview.com/corner/truth-about-separating-kids/',
'https://www.nationalreview.com/bench-memos/this-day-in-liberal-judicial-activism-june-5/',
'https://www.nationalreview.com/2018/05/tv-review-john-mccain-documentary-grit-and-dignity/',
'https://www.nationalreview.com/corner/religious-freedom-restoration-act-democrats-attack/',
'https://www.nationalreview.com/news/michael-avenatti-law-firm-must-pay-10-million-former-partner/',
'https://www.nationalreview.com/bench-memos/a-look-at-president-trumps-15th-wave-of-judicial-nominees/',
'https://www.nationalreview.com/news/china-trade-talks-white-house-tariffs/',
'https://www.nationalreview.com/news/mlk-niece-to-starbucks-fight-racism-by-ending-planned-parenthood-funding/',
'https://www.nationalreview.com/corner/background-on-the-border-controversy/',
'https://www.nationalreview.com/corner/elizabeth-warren-economics-health-care/',
'https://www.nationalreview.com/news/trump-administration-to-cut-off-abortion-providers-from-family-planning-funds/',
'https://www.nationalreview.com/photos/recreating-napoleon-invasion-of-malta-1798/',
'https://www.nationalreview.com/corner/joy-reid-blog-comments-hillary-clinton-male-ambitions/',
'https://www.nationalreview.com/news/trump-administration-slaps-steel-aluminum-tariffs-on-e-u-canada-mexico/',
'https://www.nationalreview.com/news/mike-pompeo-russia-trump-ahead-obama/',
'https://www.nationalreview.com/photos/fuego-volcano-guatemala-eruptions/',
'https://www.nationalreview.com/corner/stanley-kurtz-on-north-carolinas-campus-free-speech-act/',
'https://www.nationalreview.com/2018/06/health-care-surprise-billing-enrichs-hospitals-at-patient-expense/',
'https://www.nationalreview.com/magazine/2018/06/11/richard-pipes-communism-remembering-great-scholar/',
'https://www.nationalreview.com/news/tom-steyer-compares-impeachment-crusade-to-civil-rights-movement/',
'https://www.nationalreview.com/corner/mueller-investigation-arguments-for-ending-probe/',
'https://www.nationalreview.com/corner/rudy-giuliani-tv-appearances-make-trump-look-guilty/',
'https://www.nationalreview.com/2018/05/lies-false-criminal-allegations-reform-begins-with-exposure/',
'https://www.nationalreview.com/2018/05/illegal-immigration-enforcement-separating-kids-at-border/',
'https://www.nationalreview.com/2018/05/post-war-order-over-not-caused-by-trump-foreign-policy/',
'https://www.nationalreview.com/corner/bond-markets-and-italian-populism/',
'https://www.nationalreview.com/the-morning-jolt/trumps-email-scandal/',
'https://www.nationalreview.com/2018/05/donald-trump-makes-democrats-defend-indefensible/',
'https://www.nationalreview.com/2018/05/iran-policy-mike-pompeo-signals-tougher-stance/',
'https://www.nationalreview.com/2018/06/gay-rights-constitutional-amendment-oppressing-religious-dissent/',
'https://www.nationalreview.com/corner/chris-murphy-comments-show-why-gun-control-advocates-mistrusted/',
'https://www.nationalreview.com/corner/conservative-ideas-and-the-question-of-confidence/',
'https://www.nationalreview.com/news/tomi-lahren-minneapolis-abuse-trump-kathy-griffin-support/',
'https://www.nationalreview.com/2018/06/hillary-clinton-harvard-speech-alexander-solzhenitsyn-was-better/',
'https://www.nationalreview.com/corner/guttmacher-study-global-abortion-rates-misleading/',
'https://www.nationalreview.com/2018/05/trump-russia-investigation-collusion-narrative-collapses/',
'https://www.nationalreview.com/news/fbi-greatly-overestimated-threat-posed-by-encrypted-cell-phones/',
'https://www.nationalreview.com/news/scotus-refuses-arkansas-abortion-law-challenge/',
'https://www.nationalreview.com/news/police-confiscate-ar-15-and-ammo-from-potential-ohio-school-shooter/',
'https://www.nationalreview.com/news/parkland-students-to-announce-20-state-gun-control-tour/',
'https://www.nationalreview.com/2018/06/human-dignity-tribal-politics-decency-can-win-out/',
'https://www.nationalreview.com/magazine/2018/06/11/between-liberalism-and-democracy/',
'https://www.nationalreview.com/news/louisiana-abortion-ban-15-weeks-signed-law/',
'https://www.nationalreview.com/2018/05/north-korean-summit-should-stay-cancelled/',
'https://www.nationalreview.com/corner/supreme-court-decision-epic-systems-lewis-case/',
'https://www.nationalreview.com/bench-memos/masterpiece-cakeshop-victory/',
'https://www.nationalreview.com/corner/mccarthy-report-introduction/',
'https://www.nationalreview.com/2018/05/left-wing-extremism-anti-semitism-intersectionality/',
'https://www.nationalreview.com/news/parkland-students-democrats-seek-hire-summer/',
'https://www.nationalreview.com/news/supreme-court-arbitration-case-gorsuch-writes-opinion/',
'https://www.nationalreview.com/news/vladimir-putin-praises-donald-trump-as-good-businessman/',
'https://www.nationalreview.com/news/north-korea-kim-jong-un-aides-head-to-singapore-and-us/',
'https://www.nationalreview.com/2018/06/youtube-conservatives-changing-right-wing-disposition/',
'https://www.nationalreview.com/news/debbie-wasserman-schultz-shield-tech-aide-capitol-hill-hacking-probe/',
'https://www.nationalreview.com/2018/06/democratic-and-republican-elites-seek-to-divide-nation/',
'https://www.nationalreview.com/corner/bill-de-blasio-2020-delusions-democratic-nomination-unlikely/',
'https://www.nationalreview.com/corner/more-twisted-logic-on-obamacare/',
'https://www.nationalreview.com/news/arizona-republic-corrects-misleading-lost-kids-article/',
'https://www.nationalreview.com/2018/05/nfl-national-anthem-protest-move-understandable/',
'https://www.nationalreview.com/news/ice-director-defends-trump-ms-13-animals-remark/',
'https://www.nationalreview.com/the-morning-jolt/social-security-insolvency-date-reforms-little-support/',
'https://www.nationalreview.com/2018/05/immigration-policy-missing-kids-story-fake-real-problems/',
'https://www.nationalreview.com/news/starbucks-will-close-all-u-s-stores-tuesday-for-anti-bias-training/',
'https://www.nationalreview.com/news/opioid-epidemic-fda-cracks-down-black-market-websites/',
'https://www.nationalreview.com/bench-memos/supreme-court-historical-society-event-on-scalia-speaks/',
'https://www.nationalreview.com/bench-memos/this-day-in-liberal-judicial-activism-may-26/',
'https://www.nationalreview.com/corner/federal-officials-should-not-misrepresent-gang-affiliation-to-facilitate-deportation/',
'https://www.nationalreview.com/news/obamacare-premiums-rising-continue-2019/',
'https://www.nationalreview.com/2018/06/teacher-pay-debate-requires-careful-attention-to-facts/',
'https://www.nationalreview.com/corner/joy-reid-democrats-conspiracy-theories/',
'https://www.nationalreview.com/corner/planned-parenthood-3-percent-lie-exposed-title-x-funding/',
'https://www.nationalreview.com/magazine/2018/06/25/conservative-policies-health-care-education-debt-action-needed/',
'https://www.nationalreview.com/news/brooke-baldwin-cnn-blasts-samantha-bees-outrageous-attack-on-ivanka/',
'https://www.nationalreview.com/news/bill-clinton-defends-his-record-when-asked-about-me-too-movement/',
'https://www.nationalreview.com/2018/05/russia-investigation-robert-mueller-reach-natural-conclusion/',
'https://www.nationalreview.com/2018/05/welfare-reform-reauthorization-republicans-ambitious-risky/',
'https://www.nationalreview.com/corner/liberals-believe-tolerance-requires-republicans-be-banned/',
'https://www.nationalreview.com/2018/05/americans-conflicted-views-of-british-royal-family-monarchy/',
'https://www.nationalreview.com/news/abc-cancels-roseanne-after-stars-racist-joke/',
'https://www.nationalreview.com/2018/06/donald-trump-self-pardon-claim-congress/',
'https://www.nationalreview.com/2018/05/college-graduates-should-first-learn-how-world-works/',
'https://www.nationalreview.com/corner/federal-reserve-inflation-target-price-level-target/',
'https://www.nationalreview.com/corner/has-anyone-noticed-that-income-inequality-stopped-growing/',
'https://www.nationalreview.com/2018/06/fertility-population-how-many-kids-do-women-want/',
'https://www.nationalreview.com/2018/05/national-review-spring-webathon-reader-support-indispensable/',
'https://www.nationalreview.com/2018/05/donald-trump-department-of-justice-investigation-demand/',
'https://www.nationalreview.com/2018/05/fbi-active-shooter-data-shows-importance-of-armed-citizens/',
'https://www.nationalreview.com/the-morning-jolt/howard-schultz-president-2020-democrats-wont-embrace/',
'https://www.nationalreview.com/corner/end-the-moonshine-policy-too/',
'https://www.nationalreview.com/bench-memos/judicial-nominations-update-21/',
'https://www.nationalreview.com/news/gina-haspel-sworn-cia-first-female-director/',
'https://www.nationalreview.com/news/trump-kim-meeting-may-not-happen-june-12-us/',
'https://www.nationalreview.com/magazine/2018/06/11/middle-east-foreign-policy-us-strategy-minimizing-iran/',
'https://www.nationalreview.com/2018/06/freedom-does-not-stop-at-the-bakery-door/',
'https://www.nationalreview.com/2018/05/media-coverage-trump-russia-collusion-story-ignores-doj-fbi-hillary-collusion/',
'https://www.nationalreview.com/news/media-misrepresents-colion-noir-comments-on-news-censorship/',
'https://www.nationalreview.com/bench-memos/transgender-legal-follies-continued/',
'https://www.nationalreview.com/the-morning-jolt/for-mueller-timing-is-everything/',
'https://www.nationalreview.com/2018/06/european-democracy-in-decline-elite-attitudes/',
'https://www.nationalreview.com/corner/california-and-conservatism/',
'https://www.nationalreview.com/news/chris-matthews-democratic-partys-elitism-outrageous/',
'https://www.nationalreview.com/corner/college-students-dont-always-get-credit-for-ap-courses-why-not/',
'https://www.nationalreview.com/bench-memos/this-day-in-liberal-judicial-activism-may-19/',
'https://www.nationalreview.com/2018/05/trump-russia-investigation-clinton-email-fbi-linked-cases/',
'https://www.nationalreview.com/2018/05/trump-trade-war-threats-misguided/',
'https://www.nationalreview.com/news/james-comey-trump-fbi-scandal-defends-informant-use/',
'https://www.nationalreview.com/2018/05/robert-mueller-russia-probe-democrats-dominate-staff/',
'https://www.nationalreview.com/bench-memos/demand-justice-smears-judicial-nominee-farr/',
'https://www.nationalreview.com/news/gop-lawmakers-accuse-environmental-group-of-aiding-in-chinese-propaganda-efforts/',
'https://www.nationalreview.com/corner/clarifying-the-title-x-rule/',
'https://www.nationalreview.com/news/trump-twitter-blocking-unconstitutional-judge-ruling/',
'https://www.nationalreview.com/news/giuliani-muellers-team-agreed-to-narrow-the-scope-of-trump-interview-questions/',
'https://www.nationalreview.com/2018/06/pro-life-movement-should-take-stand-in-northern-ireland/',
'https://www.nationalreview.com/2018/06/bill-clinton-lessons-do-not-defend-indefensible/',
'https://www.nationalreview.com/news/donald-trump-commutes-alice-johnson-sentace-after-kim-kardashian/',
'https://www.nationalreview.com/news/keith-ellison-minnesota-attorney-general-campaign-announced/',
'https://www.nationalreview.com/2018/06/masterpiece-cakeshop-supreme-court-decision-free-speech-temporary-respite/',
'https://www.nationalreview.com/corner/public-university-ideological-discrimination-case/',
'https://www.nationalreview.com/bench-memos/this-day-in-liberal-judicial-activism-june-3/',
'https://www.nationalreview.com/2018/06/gerald-ford-accidental-president-nation-embraced-normality/',
'https://www.nationalreview.com/2018/06/koch-campus-controversy-conservative-donors-higher-education/',
'https://www.nationalreview.com/the-morning-jolt/shots-fired-at-a-trump-property-nothing-to-see-here/',
'https://www.nationalreview.com/corner/new-jersey-tax-hike-democrats-abandon/',
'https://www.nationalreview.com/bench-memos/denver-events-on-scalia-speaks/',
'https://www.nationalreview.com/bench-memos/this-day-in-liberal-judicial-activism-may-25/',
'https://www.nationalreview.com/news/greg-abbott-gun-safety-plan-unveiled-texas/',
'https://www.nationalreview.com/bench-memos/neil-gorsuch-supreme-court-jurisprudence/',
'https://www.nationalreview.com/corner/melania-trump-missing-media-obsesses-pointlessly/',
'https://www.nationalreview.com/magazine/2018/06/11/russian-aggression-ukraine-not-america-fault/',
'https://www.nationalreview.com/2018/06/george-papadopoulos-case-needs-closer-look/',
'https://www.nationalreview.com/news/michael-cohens-business-partner-to-cooperate-with-prosecutors/',
'https://www.nationalreview.com/corner/unc-athletics-scandal-class-cancellation-no-academic-freedom-problem/',
'https://www.nationalreview.com/news/democratic-calif-state-senator-recalled-over-support-for-gas-tax-hike/',
'https://www.nationalreview.com/magazine/2018/06/11/richard-uihlein-trump-republican-donor-shakes-up-politics/',
'https://www.nationalreview.com/magazine/2018/06/11/yale-racial-grievances-university-bows-diversity-enforcers/',
'https://www.nationalreview.com/magazine/2018/06/11/upside-of-the-upsized/',
'https://www.nationalreview.com/corner/fgm-shouldnt-have-a-place-in-the-u-s-or-anywhere/',
'https://www.nationalreview.com/news/lawsuit-border-patrol-seized-immigrants-life-savings-without-cause/',
'https://www.nationalreview.com/2018/06/objectivity-among-white-mythologies/',
'https://www.nationalreview.com/news/trump-disinvites-philadelphia-eagles-from-white-house-over-national-anthem-controversy/',
'https://www.nationalreview.com/the-morning-jolt/trumps-words-dont-mean-much-anymore/',
'https://www.nationalreview.com/2018/05/trump-planned-parenthood-decision-good-start-towards-defunding/',
'https://www.nationalreview.com/2018/06/peppermint-progressives-comparing-immigrants-gang-members/',
'https://www.nationalreview.com/news/economy-jobs-report-more-openings-than-seekers/',
'https://www.nationalreview.com/2018/06/can-a-president-pardon-himself-yes-trump-can/',
'https://www.nationalreview.com/2018/05/third-wave-feminism-progressive-agenda-devalue-conservative-women/',
'https://www.nationalreview.com/news/north-korea-summit-democrats-list-demands/',
'https://www.nationalreview.com/2018/05/north-korea-talks-china-subverts-american-positions-in-region/',
'https://www.nationalreview.com/corner/phillips-curve-model-breakdown-inflation-unemployment/',
'https://www.nationalreview.com/bench-memos/this-day-in-liberal-judicial-activism-may-18/',
'https://www.nationalreview.com/bench-memos/republican-stacking-federal-courts-claims-wrong/',
'https://www.nationalreview.com/2018/05/democrats-israel-tipping-point/',
'https://www.nationalreview.com/corner/lost-kids-op-ed-corrected/',
'https://www.nationalreview.com/corner/let-the-labor-market-continue-to-tighten/',
'https://www.nationalreview.com/corner/none-dare-call-it-illiberal-democracy/',
'https://www.nationalreview.com/2018/05/arne-duncan-pushes-parents-to-boycott-schools-over-gun-control/',
'https://www.nationalreview.com/news/donald-trump-border-wall-request/',
'https://www.nationalreview.com/news/trump-calls-for-russia-to-rejoin-g7-exacerbating-rift-with-allies/',
'https://www.nationalreview.com/2018/05/trump-has-eliminated-obama-practice-of-apologizing/',
'https://www.nationalreview.com/2018/05/trump-russia-investigation-obama-administration-origins/',
'https://www.nationalreview.com/magazine/2018/06/25/disability-benefit-reform-encourage-work/',
'https://www.nationalreview.com/corner/the-wheels-begin-to-come-off-in-the-house/',
'https://www.nationalreview.com/corner/nature-rights-radical-environmentalist-strategy/',
'https://www.nationalreview.com/2018/06/ice-loses-1500-children-myth-shows-media-bias/',
'https://www.nationalreview.com/the-morning-jolt/would-you-ever-agree-to-be-a-teenager-again/',
'https://www.nationalreview.com/corner/school-shootings-governor-doug-ducey-intelligent-policy-response/',
'https://www.nationalreview.com/2018/05/jack-johnson-pardoned-trump-century-after-racist-conviction/',
'https://www.nationalreview.com/2018/05/trump-campaign-spying-obama-administration-ignored-norms/'])

def get_article(url):
#Sends request for url
    html = requests.get(url).text
    return html

def parse_article(html):
#BeautifulSoups the article
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h1', class_='article-header__title').text
    body = soup.find('div', class_='article-content').text

    article = {
        'title': title,
        'body': body,
        'source': 'National Review',
        'num_source': 10
    }

    return article

def get_parsed_article_from_link(url):
#Runs the previous two functions on the url
    return parse_article(get_article(url))

#phase 1: uses request to try to BeautifulSoup links
NR_list_o_articles = []
NR_problem_articles = []
for text in NR_links:
    #print(text)
    try:
        art = get_parsed_article_from_link(text.encode())
        NR_list_o_articles.append(art)

    except:
        print("Problem processing url " + text)
        problem = text
        NR_problem_articles.append(problem)
    time.sleep(2)
#phase 2: uses selenium to go through links
driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
for x in NR_problem_articles:
    try:
        driver.get(x)
        time.sleep(3)
        soupy = BeautifulSoup(driver.page_source, 'lxml')
        title = soupy.find('h1', class_='article-header__title').text
        body = soupy.find('div', class_='article-content').text

        articley = {
        'title': title,
        'body': body,
        'source': 'National Review',
        'num_source': 10
        }
        NR_list_o_articles.append(articley)
    except:
        pass
#Same as above but for expanded list, phase 1
NR_more_list_o_articles = []
NR_more_problem_articles = []
for text in more_NR_links:
    #print(text)
    try:
        art = get_parsed_article_from_link(text.encode())
        NR_more_list_o_articles.append(art)

    except:
        print("Problem processing url " + text)
        problem = text
        NR_more_problem_articles.append(problem)
    time.sleep(2)
#same as above for expanded list, phase 2
driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
for x in NR_more_problem_articles:
    try:
        driver.get(x)
        time.sleep(3)
        soupy = BeautifulSoup(driver.page_source, 'lxml')
        title = soupy.find('h1', class_='article-header__title').text
        body = soupy.find('div', class_='article-content').text

        articley = {
        'title': title,
        'body': body,
        'source': 'National Review',
        'num_source': 10
        }
        NR_more_list_o_articles.append(articley)
    except:
        pass
#Puts all aticles into one list
all_articles = NR_list_o_articles + NR_more_list_o_articles

#starts client in Mongodb
client = MongoClient()
biased_news = client.project5.biased_news
#creates event and loads articles into Mongodb
db = client.events
biased_news = db.biased_news
biased_news.insert_many(all_articles)
