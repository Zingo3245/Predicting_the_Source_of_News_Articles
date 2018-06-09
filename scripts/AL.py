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

al_first_articles = ['https://altoday.com/archives/24351-democratic-lawmakers-seek-criminal-corruption-probe-of-epas-scott-pruitt',
 'https://altoday.com/archives/24322-state-rep-ed-henry-indicted-in-federal-pill-mill-case',
 'https://altoday.com/archives/24308-house-republicans-in-eleventh-hour-attempt-for-immigration-accord',
 'https://altoday.com/archives/24357-winners-losers-and-jokers-this-week-june-8-edition',
 'https://altoday.com/archives/24336-doj-lifts-secrecy-on-foreign-lobbying-opinions',
 'https://altoday.com/archives/24349-ag-steve-marshall-testifies-on-capitol-hill-in-support-of-alabama-census-lawsuit',
 'https://altoday.com/archives/24310-doj-offers-new-briefing-as-lawmakers-dispute-donald-trump-spy-claim',
 'https://altoday.com/archives/24307-donald-trump-takes-his-own-brand-of-diplomacy-to-north-korea-summit',
 'https://altoday.com/archives/24311-annemarie-axon-confirmed-as-u-s-district-judge',
 'https://altoday.com/archives/24338-donald-trump-says-let-russia-back-in-as-he-heads-for-g-7-summit',
 'https://altoday.com/archives/24334-doug-jones-says-donald-trumps-tariffs-threaten-alabamas-auto-industry']

al_more_articles = ['https://altoday.com/archives/22879-terri-sewell-introduces-bill-to-allow-direct-medicare-payments-to-physician-assistants',
 'https://altoday.com/archives/21932-how-todays-loudest-progressives-are-nothing-like-those-who-fought-for-civil-rights',
 'https://altoday.com/archives/22400-whats-next-house-speaker-paul-ryan',
 'https://altoday.com/archives/23542-donald-trump-nominates-alabamas-corey-maze-for-federal-judgeship',
 'https://altoday.com/archives/23864-donald-trump-no-immigration-deal-unless-real-wall-good-security',
 'https://altoday.com/archives/24176-immigration-fight-tension-on-tariffs-await-congress-return',
 'https://altoday.com/archives/23370-a-year-after-obamacare-vote-democrats-see-election-cudgel',
 'https://altoday.com/archives/22076-women-in-politics-and-metoo',
 'https://altoday.com/archives/23829-dems-want-to-scrap-tax-cut-for-rich-to-fund-teachers-raises',
 'https://altoday.com/archives/22226-alabama-legislature-approves-rural-hospital-resource-center',
 'https://altoday.com/archives/22387-racial-profiling-bill-dies-alabama-legislature',
 'https://altoday.com/archives/22830-five-members-of-alabama-delegation-receive-award-for-conservative-excellence',
 'https://altoday.com/archives/24203-parkland-students-to-make-bus-tour-to-register-young-voters',
 'https://altoday.com/archives/22825-donald-trump-builds-on-barack-obama-opioid-policy',
 'https://altoday.com/archives/23144-va-nominee-accused-of-drunken-behavior-reckless-prescribing',
 'https://altoday.com/archives/23332-donald-trump-acknowledges-he-repaid-lawyer-for-stormy-daniels-hush-money',
 'https://altoday.com/archives/22829-celebrating-john-archibalds-pulitzer-while-mourning-the-lack-of-talent-in-most-newsrooms',
 'https://altoday.com/archives/21731-doug-jones-visits-birmingham-school-to-celebrate-read-across-america-day',
 'https://altoday.com/archives/23068-aimed-at-china-donald-trumps-tariffs-are-hitting-closer-to-home',
 'https://altoday.com/archives/23706-hey-john-cooper-aldot-governor-kay-ivey-you-guys-have-one-job',
 'https://altoday.com/archives/23040-ag-steve-marshall-to-host-faith-forums-in-hopes-of-tackling-crime-addiction',
 'https://altoday.com/archives/22200-state-senate-votes-to-reform-controversial-practice-of-civil-asset-forfeiture',
 'https://altoday.com/archives/21786-house-bill-seeks-to-rebalance-renter-tenant-protections',
 'https://altoday.com/archives/23702-north-korea-threatens-to-cancel-trump-kim-summit-over-drills',
 'https://altoday.com/archives/23025-travel-ban-case-is-justices-first-dive-into-trump-policy',
 'https://altoday.com/archives/23799-will-the-real-kay-ivey-please-speak-up-the-wide-divide-between-iveys-official-and-campaign-messages',
 'https://altoday.com/archives/24158-donald-trump-asserts-absolute-right-to-pardon-himself',
 'https://altoday.com/archives/23961-rudy-giuliani-says-white-house-wants-briefing-on-classified-info',
 'https://altoday.com/archives/24268-trustees-report-warns-medicare-social-security-finances-worsening',
 'https://altoday.com/archives/24077-donald-trump-signs-bill-for-terminal-patients-to-try-unproven-drugs',
 'https://altoday.com/archives/23270-progressive-comedians-have-lost-sight-of-whats-funny-or-decent',
 'https://altoday.com/archives/23169-donald-trump-says-of-james-comey-hes-either-very-sick-or-very-dumb',
 'https://altoday.com/archives/24224-conservative-icon-david-koch-leaving-business-politics',
 'https://altoday.com/archives/22856-steve-scalise-undergoes-planned-surgery-10-months-after-shooting',
 'https://altoday.com/archives/22343-house-delays-vote-continues-negotiations-on-bill-to-track-race-at-traffic-stops',
 'https://altoday.com/archives/22731-exclusive-state-auditors-office-jim-zeigler-kicked-of-state-house',
 'https://altoday.com/archives/22689-kevin-mccarthy-steve-scalise-likely-contenders-house-speaker',
 'https://altoday.com/archives/21848-jeff-sessions-california-immigration-policy-defies-common-sense',
 'https://altoday.com/archives/23380-after-flirting-with-gun-control-movement-donald-trump-faces-nra',
 'https://altoday.com/archives/23844-donald-trump-seethes-over-russia-probe-calls-for-end-to-spygate',
 'https://altoday.com/archives/23931-alabamians-urge-richard-shelby-to-fully-fund-global-hiv-aids-program',
 'https://altoday.com/archives/23437-donald-trump-defends-cia-nominee-says-she-is-tough-on-terror',
 'https://altoday.com/archives/22401-donald-trump-warns-may-freeze-skorea-trade-deal-nkorea-talks',
 'https://altoday.com/archives/22315-state-house-to-reconsider-traffic-stop-racial-profiling-bill',
 'https://altoday.com/archives/21152-a-new-project-conservatives-for-better-leadership',
 'https://altoday.com/archives/24011-donald-trump-renews-china-tariff-threat-complicating-talks',
 'https://altoday.com/archives/23463-donald-trump-says-hell-speak-tuesday-with-president-xi-jinping-of-china',
 'https://altoday.com/archives/23781-donald-trump-to-doj-investigate-whether-fbi-infiltrated-campaign',
 'https://altoday.com/archives/24073-u-s-to-push-steel-aluminum-tariffs-on-e-u-canada-and-mexico',
 'https://altoday.com/archives/23591-donald-trump-honors-his-late-mother-in-mothers-day-video',
 'https://altoday.com/archives/23564-in-taking-on-high-drug-prices-donald-trump-faces-a-complex-nemesis',
 'https://altoday.com/archives/23865-human-rights-an-afterthought-ahead-of-us-north-korea-summit',
 'https://altoday.com/archives/23234-trump-gives-thumbs-down-to-comic-who-roasted-his-spokeswoman',
 'https://altoday.com/archives/23084-randall-woodfin-takes-unorthodox-approach-give-me-me-your-gun-ill-help-you-find-a-job',
 'https://altoday.com/archives/22391-divided-alabama-senate-approves-ethics-exemption-2',
 'https://altoday.com/archives/22515-china-us-tariff-spat-mostly-losers-winners',
 'https://altoday.com/archives/22146-state-senate-votes-term-limits-lawmakers',
 'https://altoday.com/archives/20816-harley-barber-expulsion-from-university-of-alabama-a-missed-opportunity',
 'https://altoday.com/archives/22891-alabama-politicians-react-to-the-death-of-barbara-bush',
 'https://altoday.com/archives/24111-north-koreans-to-meet-donald-trump-deliver-letter-from-leader',
 'https://altoday.com/archives/21994-state-house-votes-reinstate-school-safety-task-force',
 'https://altoday.com/archives/22426-alabama-legislator-jack-williams-ex-gop-chair-marty-connors-arrested-on-federal-bribery-charges',
 'https://altoday.com/archives/21960-us-sets-new-record-censoring-withholding-govt-files',
 'https://altoday.com/archives/23567-us-embassy-in-jerusalem-to-open-with-initial-staff-of-50',
 'https://altoday.com/archives/23963-more-lgbt-issues-loom-as-justices-near-wedding-cake-decision',
 'https://altoday.com/archives/23240-alabama-to-add-107-new-first-class-pre-k-classrooms-in-2018-2019-school-year',
 'https://altoday.com/archives/22314-odds-john-bolton-north-korea-jim-mattis-appears-isolated',
 'https://altoday.com/archives/23869-donald-trump-calls-off-historic-summit-with-north-korea',
 'https://altoday.com/archives/23891-finally-the-nfl-takes-a-stand-against-the-knee',
 'https://altoday.com/archives/22855-supreme-court-hearing-case-about-online-sales-tax-collection',
 'https://altoday.com/archives/22944-donald-trump-leaves-possibility-of-bailing-on-meeting-with-kim-open',
 'https://altoday.com/archives/22357-donald-trump-emerging-seclusion-promote-infrastructure-plan',
 'https://altoday.com/archives/21993-prosecuting-lie-buy-guns-strain-resources',
 'https://altoday.com/archives/22258-alabama-house-rejects-bill-track-race-traffic-stops',
 'https://altoday.com/archives/21298-heres-how-alabama-has-the-power-to-prevent-another-charlottesville',
 'https://altoday.com/archives/23970-donald-trump-threatens-another-shutdown-as-budget-battle-heats-up',
 'https://altoday.com/archives/24106-u-s-allies-to-fight-donald-trumps-tariffs-plan-warn-of-trade-war',
 'https://altoday.com/archives/23080-opioid-treatment-gap-in-medicare-methadone-clinics',
 'https://altoday.com/archives/22048-pay-raise-for-teachers-approved-by-alabama-lawmakers',
 'https://altoday.com/archives/22691-30000-rumor-tabloid-paid-spiked-salacious-donald-trump-tip',
 'https://altoday.com/archives/20572-florida-governor-rick-scott-says-not-champs',
 'https://altoday.com/archives/22647-ap-sources-house-speaker-paul-ryan-wont-run-re-election',
 'https://altoday.com/archives/23693-donald-trump-jr-cant-recall-discussing-russia-probe-with-father',
 'https://altoday.com/archives/22452-kay-ivey-signs-legislation-creating-alabama-school-of-cyber-technology-and-engineering-education-budget',
 'https://altoday.com/archives/23333-u-s-china-trade-talks-center-on-rivalry-over-technology',
 'https://altoday.com/archives/22858-how-a-supreme-court-case-could-affect-your-online-purchases',
 'https://altoday.com/archives/24095-state-launches-summer-literacy-pilot-program-to-prevent-dreaded-summer-slide',
 'https://altoday.com/archives/23589-mike-pompeo-nkorea-needs-us-security-assurances-for-nuke-pact',
 'https://altoday.com/archives/23042-birminghams-maynard-cooper-expands-new-office-in-washington-d-c',
 'https://altoday.com/archives/22646-jeff-sessions-address-immigration-border-sheriffs-meeting',
 'https://altoday.com/archives/23595-second-democratic-senator-publicly-backing-donald-trumps-cia-pick',
 'https://altoday.com/archives/22055-bill-to-strip-lieutenant-governor-of-powers-delayed-in-state-senate',
 'https://altoday.com/archives/23367-were-you-lying-sanders-faces-new-credibility-questions',
 'https://altoday.com/archives/23917-summit-talk-turns-warmer-donald-trump-says-talking-to-them-now',
 'https://altoday.com/archives/23020-mike-pompeo-facing-rare-opposition-from-senate-panel',
 'https://altoday.com/archives/22194-leaders-finalize-u-s-budget-bill-voting-could-begin-thursday',
 'https://altoday.com/archives/22131-alabama-lawmakers-approve-nitrogen-execution-for-death-row-inmates',
 'https://altoday.com/archives/22813-lawmakers-assign-11-million-for-behavioral-health-services',
 'https://altoday.com/archives/22694-pompeo-defends-trump-russia-wont-talk-mueller',
 'https://altoday.com/archives/21282-doug-jones-weighs-long-term-bipartisan-senate-budget-compromise',
 'https://altoday.com/archives/23637-donald-trump-pays-tribute-to-fallen-officers-in-emotional-ceremony',
 'https://altoday.com/archives/22370-incentives-bill-to-encourage-rural-broadband-expansion-becomes-state-law',
 'https://altoday.com/archives/23749-conservative-revolt-over-immigration-sinks-house-farm-bill',
 'https://altoday.com/archives/22551-u-s-approves-1-3-billion-sale-artillery-saudi-arabia',
 'https://altoday.com/archives/22033-hoping-the-walkout-was-a-wake-up-for-todays-youth',
 'https://altoday.com/archives/23584-u-s-hopes-north-korea-will-become-close-partner-mike-pompeo-says',
 'https://altoday.com/archives/23001-bill-signing-ceremony-celebrates-new-guardianship-law-to-assist-those-with-disabilities',
 'https://altoday.com/archives/21436-stop-vilifying-gun-owners-and-nra-members-every-shooting',
 'https://altoday.com/archives/23818-donald-trump-wades-deeper-into-abortion-politics-as-midterms-loom',
 'https://altoday.com/archives/23390-terri-sewell-martha-roby-fly-f-35-cockpit-simulator',
 'https://altoday.com/archives/24119-trump-administration-considers-plan-to-bail-out-struggling-coal-nuclear-plants',
 'https://altoday.com/archives/22256-alabamians-to-vote-on-ten-commandments-ballot-proposal-in-nov',
 'https://altoday.com/archives/22035-child-care-safety-act-passes-senate-heads-to-kay-iveys-desk',
 'https://altoday.com/archives/21991-alabama-fantasy-sports-bill-fails-senate-ahead-vote',
 'https://altoday.com/archives/22346-donald-trump-says-second-amendment-wont-repealed',
 'https://altoday.com/archives/23672-terri-sewell-mike-rogers-introduce-bipartisan-bill-to-address-issue-plaguing-rural-america',
 'https://altoday.com/archives/22083-donald-trump-opioid-plan-includes-death-penalty-traffickers',
 'https://altoday.com/archives/22627-u-s-senate-needs-welcome-baby-duckworth-open-arms',
 'https://altoday.com/archives/24088-kay-ivey-signs-increased-penalties-for-human-trafficking-into-law',
 'https://altoday.com/archives/22449-donald-trump-discuss-tax-cuts-west-virginia-round-table',
 'https://altoday.com/archives/23021-mo-brooks-urges-doug-jones-to-confirm-mike-pompeo-as-secretary-of-state',
 'https://altoday.com/archives/23469-kay-iveys-school-safety-council-releases-first-10-recommendations',
 'https://altoday.com/archives/22273-key-redistricting-case-goes-front-high-court',
 'https://altoday.com/archives/22441-democrats-raise-ethics-questions-trump-defense-fund',
 'https://altoday.com/archives/24021-both-sides-preparing-as-if-u-s-north-korea-summit-is-a-go',
 'https://altoday.com/archives/22616-kay-ivey-signs-amendments-to-simplified-sellers-use-tax-program',
 'https://altoday.com/archives/24183-supreme-court-gives-victory-to-baker-who-refused-to-make-cake-for-gay-wedding',
 'https://altoday.com/archives/23453-betsy-devos-calls-kay-ivey-tells-her-us-dept-of-education-approved-alabama-essa-plan',
 'https://altoday.com/archives/23041-here-are-alabamas-student-winners-of-the-2018-congressional-art-competition',
 'https://altoday.com/archives/23552-5-craziest-take-aways-from-the-roy-johnson-piece-on-paul-littlejohn-iii',
 'https://altoday.com/archives/23734-lgbtq-nonprofit-rescinds-patricia-todds-job-offer-after-tweet-trying-to-out-kay-ivey',
 'https://altoday.com/archives/24135-donald-trump-hints-at-longer-path-for-north-korea-to-de-nuke',
 'https://altoday.com/archives/22482-donald-trump-says-strong-action-coming-immigration',
 'https://altoday.com/archives/22235-steve-bannon-blames-gop-leaders-roy-moores-defeat-alabama',
 'https://altoday.com/archives/23300-special-counsel-team-has-floated-idea-of-subpoena-for-donald-trump',
 'https://altoday.com/archives/23298-fed-set-to-leave-rates-alone-amid-signs-of-rising-inflation',
 'https://altoday.com/archives/21762-upskirting-victims-push-fill-loophole-alabama-law',
 'https://altoday.com/archives/22350-alabama-senate-passes-resolution-condemning-doug-jones-abortion-vote',
 'https://altoday.com/archives/24219-u-n-calls-on-u-s-to-halt-separations-of-migrant-families',
 'https://altoday.com/archives/22264-heres-how-the-1-3-trillion-government-funding-bill-impacts-alabama',
 'https://altoday.com/archives/22178-gun-control-arming-teachers-bills-dead-session',
 'https://altoday.com/archives/22468-state-rep-jack-williams-denies-wrongdoing-amid-federal-bribery-charges',
 'https://altoday.com/archives/21806-democratic-support-senate-eyes-rollback-banking-law',
 'https://altoday.com/archives/23526-democratic-lawmakers-release-thousands-of-russian-facebook-ads',
 'https://altoday.com/archives/22359-doctor-white-house-physician-nominated-lead-va',
 'https://altoday.com/archives/23972-misleading-tweets-by-liberal-activists-fuel-donald-trump',
 'https://altoday.com/archives/21737-ill-toast-to-that-lets-pass-direct-to-consumer-wine-legislation-this-session',
 'https://altoday.com/archives/22390-lawmakers-end-session-tensions-eye-elections',
 'https://altoday.com/archives/24043-from-roseanne-to-jim-bonner-why-dont-people-think-before-they-post',
 'https://altoday.com/archives/22105-kay-ivey-signs-controversial-contract-prison-health-care-provider',
 'https://altoday.com/archives/22896-state-rep-jack-williams-ex-gop-chair-marty-connors-to-appear-in-federal-court',
 'https://altoday.com/archives/23336-paul-ryan-democratic-takeover-would-mean-subpoenas-and-chaos',
 'https://altoday.com/archives/21434-alabama-politicians-react-to-florida-school-shooting',
 'https://altoday.com/archives/22044-alabama-reactions-to-national-school-walkout',
 'https://altoday.com/archives/22010-push-for-greater-equality-adline-clarke-proposes-gender-pay-gap-bill',
 'https://altoday.com/archives/21961-fate-hazy-for-gop-bill-helping-dying-patients-try-new-drugs',
 'https://altoday.com/archives/24071-kay-ivey-announces-plan-to-arm-school-administrators',
 'https://altoday.com/archives/23126-french-president-emmanuel-macron-urges-us-to-reject-isolationism',
 'https://altoday.com/archives/23231-in-donald-trump-era-the-death-of-the-white-house-press-conference',
 'https://altoday.com/archives/22090-randall-woodfins-ambitious-100-days-promises-kept-works-progress',
 'https://altoday.com/archives/22138-lawmakers-unanimously-vote-to-close-loophole-in-states-drunk-driving-law',
 'https://altoday.com/archives/22823-gop-attorneys-general-support-citizenship-question-on-census',
 'https://altoday.com/archives/23851-on-long-island-donald-trump-to-speak-on-immigration-gang-violence',
 'https://altoday.com/archives/23421-donald-trump-says-he-wont-let-right-to-bear-arms-be-under-siege',
 'https://altoday.com/archives/20522-high-time-congress-takes-up-marijuana',
 'https://altoday.com/archives/22006-lt-gov-candidate-sen-rusty-glover-drops-plan-permanent-daylight-saving-time',
 'https://altoday.com/archives/23911-standing-with-publix-and-the-second-amendment-tomorrow-and-in-the-future',
 'https://altoday.com/archives/22116-mike-rogers-takes-hard-stand-against-smears-from-radical-liberal-groups',
 'https://altoday.com/archives/23824-donald-trump-suggests-summit-with-kim-jong-un-could-be-delayed',
 'https://altoday.com/archives/22241-state-house-passes-data-breach-protections-for-consumers',
 'https://altoday.com/archives/23263-like-a-showman-donald-trump-suggests-demilitarized-zone-for-big-event',
 'https://altoday.com/archives/22385-final-passage-given-closure-loophole-states-drunk-driving-law',
 'https://altoday.com/archives/24159-china-says-trade-deals-are-off-if-u-s-raises-tariffs',
 'https://altoday.com/archives/23105-kay-ivey-travels-to-japan-meets-with-automakers',
 'https://altoday.com/archives/23622-melania-trump-has-successful-procedure-on-kidney-condition',
 'https://altoday.com/archives/21238-house-passes-bradley-byrnes-reforms-congressional-workplace',
 'https://altoday.com/archives/23855-nfl-owners-adopt-new-policy-to-address-anthem-protests',
 'https://altoday.com/archives/23436-nancy-pelosi-says-democrats-have-cash-and-environment-to-win-house',
 'https://altoday.com/archives/22236-congress-passes-1-3-trillion-budget-averting-another-shutdown',
 'https://altoday.com/archives/22369-education-trust-fund-budget-clears-final-hurdle-heads-to-kay-iveys-desk',
 'https://altoday.com/archives/23814-kay-ivey-signs-five-bills-focusing-on-military-veterans-and-their-families',
 'https://altoday.com/archives/23752-donald-trumps-pick-to-head-veterans-affairs-robert-wilkie',
 'https://altoday.com/archives/23363-rudy-giuliani-becomes-aggressive-new-face-of-donald-trump-legal-team',
 'https://altoday.com/archives/23745-animals-donald-trump-says-hell-keep-using-term-for-gang-members',
 'https://altoday.com/archives/23509-detainees-freed-in-north-korea-returning-to-us-with-mike-pompeo',
 'https://altoday.com/archives/21842-watchdog-report-failed-va-leadership-put-patients-risk',
 'https://altoday.com/archives/23212-mike-pompeo-us-stands-with-israel-in-fight-against-iran',
 'https://altoday.com/archives/22940-trade-issues-expose-the-limits-of-donald-trump-shinzo-abe-bromance',
 'https://altoday.com/archives/23074-senators-considering-a-delay-for-va-confirmation-hearing',
 'https://altoday.com/archives/23743-donald-trump-to-deny-funds-to-clinics-that-refer-for-abortion',
 'https://altoday.com/archives/23766-cias-gina-haspel-can-tap-undercover-work-in-russian-operations',
 'https://altoday.com/archives/22981-in-james-comey-memos-donald-trump-talks-of-jailed-journalists-and-hookers',
 'https://altoday.com/archives/22853-tax-day-is-here-americans-still-largely-unaware-of-tax-reform-benefits',
 'https://altoday.com/archives/22329-alabama-education-budget-moves-one-step-closer-kay-iveys-desk',
 'https://altoday.com/archives/23678-we-need-to-focus-on-results-not-rumors',
 'https://altoday.com/archives/21493-alabamas-congressional-democrats-ready-for-gun-control-action-republicans-mum',
 'https://altoday.com/archives/23488-donald-trump-tax-reform-means-more-money-in-your-pocket',
 'https://altoday.com/archives/22472-us-proposes-tariffs-50-billion-chinese-imports',
 'https://altoday.com/archives/22977-donald-trump-says-midterm-elections-are-choice-for-country-on-taxes',
 'https://altoday.com/archives/23499-cia-nominee-says-tough-lessons-learned-from-interrogation',
 'https://altoday.com/archives/21889-senate-passes-30-days-to-pay-bill-to-reform-payday-lending',
 'https://altoday.com/archives/23681-martha-roby-returns-from-seventh-troop-visit-in-afghanistan',
 'https://altoday.com/archives/23145-prosecutor-on-justices-opioid-crackdown-favors-tough-tact',
 'https://altoday.com/archives/24069-saving-jeff-sessions-inside-the-gop-effort-to-protect-the-attorney-general',
 'https://altoday.com/archives/23287-alabamas-first-openly-gay-lawmaker-patricia-todd-to-lead-lgbtq-coalition',
 'https://altoday.com/archives/23768-where-did-donald-trumps-claim-of-an-fbi-mole-come-from',
 'https://altoday.com/archives/22498-people-deserve-debates-whether-or-not-they-get-them-is-anyones-guess',
 'https://altoday.com/archives/21562-alabama-lawmakers-pass-one-of-two-marijuana-bills',
 'https://altoday.com/archives/23777-us-issues-steep-list-of-demands-for-nuclear-treaty-with-iran',
 'https://altoday.com/archives/23458-world-to-learn-fate-of-iran-nuclear-pact-tuesday-afternoon',
 'https://altoday.com/archives/23296-next-steps-for-caravan-will-unfold-mostly-out-of-public-view',
 'https://altoday.com/archives/22172-allegations-women-past-shadow-donald-trump',
 'https://altoday.com/archives/23501-kay-ivey-alabama-stronger-than-it-was-a-year-ago',
 'https://altoday.com/archives/23226-alabamians-to-decide-the-fate-of-four-proposed-constitutional-amendments',
 'https://altoday.com/archives/23229-mike-pompeo-says-israel-palestinian-peace-still-a-u-s-priority',
 'https://altoday.com/archives/22889-former-first-lady-barbara-bush-dies-at-age-92',
 'https://altoday.com/archives/22246-heres-how-the-alabama-delegation-voted-for-the-1-3-trillion-government-funding-bill',
 'https://altoday.com/archives/23188-ten-commandments-bill-to-be-amendment-one-on-novembers-election-ballot',
 'https://altoday.com/archives/23819-terri-sewell-doug-jones-announce-public-health-fair-to-combat-wastewater-crisis',
 'https://altoday.com/archives/23960-donald-trump-says-illegal-crossings-down-theyre-up-2',
 'https://altoday.com/archives/22702-doug-jones-book-bending-toward-justice-track-january-release',
 'https://altoday.com/archives/22260-state-house-follows-senates-lead-approves-stiffer-fentanyl-penalties',
 'https://altoday.com/archives/23660-personnel-note-cate-cullen-leaves-gary-palmers-office-to-join-cruise-lines-intl-association',
 'https://altoday.com/archives/22402-president-trump-goes-favorite-target-amazon',
 'https://altoday.com/archives/23138-donald-trump-meeting-with-apples-tim-cook-on-trade',
 'https://altoday.com/archives/22967-birminghams-randall-woodfin-needs-to-prioritize-results-not-photo-ops',
 'https://altoday.com/archives/21119-one-acceptable-answer-lawmakers-daycare-bill-pass',
 'https://altoday.com/archives/22851-former-first-lady-barbara-bush-in-failing-health',
 'https://altoday.com/archives/22520-mo-brooks-praises-donald-trumps-decision-to-use-military-along-southern-border',
 'https://altoday.com/archives/24297-house-gop-factions-at-odds-as-immigration-showdown-nears',
 'https://altoday.com/archives/24082-alabama-leaders-react-to-kay-ivey-arming-school-administrators',
 'https://altoday.com/archives/21974-rosa-parks-day-approved-by-senate-committee-moves-to-senate',
 'https://altoday.com/archives/23216-buses-carrying-central-american-migrants-roll-to-u-s-border',
 'https://altoday.com/archives/21851-lawmakers-debate-change-ethics-law-economic-developer',
 'https://altoday.com/archives/22506-22506',
 'https://altoday.com/archives/22415-donald-trumps-talk-syria-pullout-nothing-new',
 'https://altoday.com/archives/22117-armed-teacher-bill-on-top-of-state-houses-legislative-calendar-tuesday',
 'https://altoday.com/archives/23583-donald-trumps-prescription-to-reduce-drug-prices-takes-small-steps',
 'https://altoday.com/archives/24299-congressional-democrats-take-donald-trump-to-court-over-foreign-favors',
 'https://altoday.com/archives/21537-two-alabama-bills-to-lower-penalties-for-marijuana-possession-up-for-debate',
 'https://altoday.com/archives/21996-cabinet-chaos-trumps-team-battles-scandal-irrelevance',
 'https://altoday.com/archives/23304-annual-supreme-court-guessing-game-will-anthony-kennedy-stay-or-go',
 'https://altoday.com/archives/22597-national-guard-members-begin-arriving-at-u-s-mexico-border',
 'https://altoday.com/archives/22271-poll-americans-open-to-donald-trumps-planned-north-korea-talks',
 'https://altoday.com/archives/22161-doug-jones-uses-first-floor-speech-to-urge-colleagues-to-take-on-gun-violence',
 'https://altoday.com/archives/23642-kay-ivey-among-7-governors-backing-donald-trumps-nomination-for-nobel-peace-prize',
 'https://altoday.com/archives/23442-devin-nunes-threatens-jeff-sessions-with-contempt-charges-over-russia',
 'https://altoday.com/archives/22880-kay-ivey-announces-grant-to-fund-alabama-drug-task-force',
 'https://altoday.com/archives/23964-doug-jones-introduces-bill-to-improve-rural-health-care',
 'https://altoday.com/archives/22684-kay-ivey-changes-stance-signs-order-prohibiting-use-of-loaned-executives',
 'https://altoday.com/archives/22481-facing-heat-home-gop-leaders-may-rescind-spending',
 'https://altoday.com/archives/22336-patricia-todd-alabamas-first-gay-legislator-bids-farewell-to-house',
 'https://altoday.com/archives/24044-mental-health-awareness-month-is-ending-but-the-work-continues',
 'https://altoday.com/archives/21906-donald-trump-plans-meet-kim-jong-un-nuke-talks',
 'https://altoday.com/archives/23827-u-s-clings-to-health-coverage-gains-despite-political-drama',
 'https://altoday.com/archives/23714-donald-trump-draws-rebuke-for-animal-remark-at-immigration-talk',
 'https://altoday.com/archives/24199-alabama-politicians-react-to-supreme-court-gay-wedding-cake-ruling',
 'https://altoday.com/archives/23168-donald-trumps-va-choice-bows-out-in-latest-cabinet-flame-out',
 'https://altoday.com/archives/22422-algop-chair-terry-lathan-applauds-republican-caucus-legislative-accomplishments',
 'https://altoday.com/archives/23593-michael-bloomberg-warns-of-epidemic-of-dishonesty',
 'https://altoday.com/archives/23823-paul-ryan-vents-frustration-over-gop-infighting-over-immigration',
 'https://altoday.com/archives/23464-hill-panel-probing-opioids-abuse-targets-distributor-firms',
 'https://altoday.com/archives/23405-after-months-of-evasion-kay-iveys-campaign-looks-alive-for-a-moment',
 'https://altoday.com/archives/22416-donal-trump-hails-border-wall-start-illusion',
 'https://altoday.com/archives/23146-jeff-sessions-defends-trump-pardons-of-joe-arpaio-scooter-libby',
 'https://altoday.com/archives/23261-u-s-starts-processing-asylum-seekers-slammed-by-donald-trump',
 'https://altoday.com/archives/22902-senate-panel-divided-over-mike-pompeo-for-secretary-of-state',
 'https://altoday.com/archives/23822-scott-pruitt-dealing-with-water-contaminant-a-national-priority',
 'https://altoday.com/archives/23527-texas-suit-could-speed-dacas-path-to-supreme-court',
 'https://altoday.com/archives/21892-senators-allow-feds-keep-guns-people-deemed-threat',
 'https://altoday.com/archives/23867-disputed-keystone-pipeline-project-focus-of-court-hearing',
 'https://altoday.com/archives/22443-donald-trump-calls-border-legislation-using-nuclear-option',
 'https://altoday.com/archives/22317-california-county-considers-fighting-states-sanctuary-law',
 'https://altoday.com/archives/22946-babies-of-senators-now-welcome-in-senate-chamber',
 'https://altoday.com/archives/22521-trump-signs-proclamation-directing-troops-secure-border',
 'https://altoday.com/archives/22633-richard-shelby-selected-to-chair-powerful-senate-spending-panel',
 'https://altoday.com/archives/23631-apology-overdue-mccain-flap-overshadows-trumps-gop-lunch',
 'https://altoday.com/archives/22403-jeff-sessions-no-new-special-counsel-yet-republican-concerns',
 'https://altoday.com/archives/22078-city-of-mobile-has-new-tool-to-tackle-blight-thanks-to-newly-signed-law',
 'https://altoday.com/archives/23406-the-white-house-should-revoke-april-ryans-press-credentials',
 'https://altoday.com/archives/21003-the-n-word',
 'https://altoday.com/archives/23302-is-donald-trump-right-about-judges-leanings-maybe-review-shows',
 'https://altoday.com/archives/23655-cia-nominee-gina-haspel-wins-senate-panel-backing-confirmation-expected',
 'https://altoday.com/archives/23717-donald-trump-if-fbi-spied-on-my-campaign-bigger-than-watergate',
 'https://altoday.com/archives/23419-donald-trump-chides-rudy-giuliani-to-get-his-facts-straight-on-stormy-daniels',
 'https://altoday.com/archives/21926-fairhopes-hiring-new-police-sergeant-making-waves-local-government',
 'https://altoday.com/archives/20138-doug-jones-mail-piece-possibly-worst-ever',
 'https://altoday.com/archives/22340-donald-trump-good-chance-nkorean-leader-will-right',
 'https://altoday.com/archives/21801-donald-trump-paul-ryan-face-off-rare-public-gop-clash-tariffs',
 'https://altoday.com/archives/22024-tillersons-dismissal-may-hasten-demise-iran-nuclear-deal',
 'https://altoday.com/archives/21266-calling-on-john-kelly-and-others-at-white-house-to-apologize-for-rob-porter-coverup',
 'https://altoday.com/archives/22577-trump-complains-stupid-trade-china',
 'https://altoday.com/archives/22291-bill-to-appoint-county-school-superintendents-to-be-considered-by-state-house',
 'https://altoday.com/archives/23636-democrats-seek-counterweight-to-donald-trumps-message-in-2020',
 'https://altoday.com/archives/22154-can-we-agree-to-ban-the-term-fake-news',
 'https://altoday.com/archives/22809-doug-jones-supports-donald-trump-actions-on-syria',
 'https://altoday.com/archives/23953-heres-who-the-alabama-retailpac-is-endorsing-for-the-2018-elections',
 'https://altoday.com/archives/22904-donald-trump-says-good-relationship-formed-with-north-korea',
 'https://altoday.com/archives/21936-donald-trump-backs-off-push-raising-assault-rifle-purchase-age',
 'https://altoday.com/archives/23152-richard-shelby-votes-in-favor-of-improved-senate-nominations-procedure',
 'https://altoday.com/archives/22667-paul-ryan-retirement-sends-new-ripples-uncertainty-gop',
 'https://altoday.com/archives/21979-house-approves-85-million-prison-improvements',
 'https://altoday.com/archives/23480-trump-withdraws-from-iran-nuclear-deal-alabama-delegation-reacts',
 'https://altoday.com/archives/22101-senators-preview-proposals-improving-election-systems',
 'https://altoday.com/archives/21455-lawmaker-introduce-bill-alabama-teachers-carry-firearms',
 'https://altoday.com/archives/23635-study-despite-modest-income-teachers-pay-for-class-needs',
 'https://altoday.com/archives/22847-former-senior-aide-to-donald-trump-jeff-sessions-takes-gig-with-dc-consulting-firm',
 'https://altoday.com/archives/22714-james-comey-compares-donald-trump-mob-boss',
 'https://altoday.com/archives/23265-welcome-to-the-partisan-fury-michelle-wolf',
 'https://altoday.com/archives/23871-alabama-delegation-votes-to-pass-major-va-overhaul-trump-expected-to-sign-into-law',
 'https://altoday.com/archives/21875-texas-primary-turnout-buoys-democrats-hopes',
 'https://altoday.com/archives/23617-sanctuary-cities-could-get-boost-from-sports-betting-ruling',
 'https://altoday.com/archives/24109-will-ainsworth-honored-kay-ivey-adopted-his-school-security-plan',
 'https://altoday.com/archives/22316-fight-fire-fire-opponents-borrow-donald-trumps-playbook',
 'https://altoday.com/archives/23764-white-house-pushes-ahead-with-mideast-peace-plan',
 'https://altoday.com/archives/22342-female-senators-want-debate-anti-harassment-bill',
 'https://altoday.com/archives/22166-background-check-measure-guns-included-spending-bill',
 'https://altoday.com/archives/23137-white-house-condemns-ruling-on-donald-trumps-dreamers-program',
 'https://altoday.com/archives/23330-kay-ivey-stands-up-for-mobile-teacher-who-was-to-change-just-pray-t-shirt',
 'https://altoday.com/archives/21879-house-gives-final-approval-to-largest-tax-cut-in-over-a-decade',
 'https://altoday.com/archives/22549-china-vows-counterattack-trump-administration-tariffs',
 'https://altoday.com/archives/23130-lax-vetting-on-trump-nominees-begins-to-frustrate-senators',
 'https://altoday.com/archives/21908-following-suicide-of-5th-grader-state-house-passes-anti-cyberbullying-legislation',
 'https://altoday.com/archives/22220-state-house-passes-school-security-funding-bill',
 'https://altoday.com/archives/24013-donald-trump-says-he-wishes-hed-picked-a-different-attorney-general',
 'https://altoday.com/archives/23841-us-south-korea-work-to-keep-north-korea-summit-on-track',
 'https://altoday.com/archives/23167-randall-woodfin-outlines-proposal-for-birminghams-2019-budget-8-million-increase-from-2018',
 'https://altoday.com/archives/22352-racial-profiling-at-traffic-stops-bill-stalls-yet-again-in-state-house',
 'https://altoday.com/archives/24078-state-cuts-burdensome-red-tape-for-alabama-businesses',
 'https://altoday.com/archives/23700-us-has-a-daunting-to-do-list-to-get-ready-for-nkorea-summit',
 'https://altoday.com/archives/23150-former-president-george-h-w-bush-out-of-intensive-care-making-progress',
 'https://altoday.com/archives/22978-poll-americans-expect-russia-tension-will-get-worse',
 'https://altoday.com/archives/22445-china-raises-tariffs-us-pork-fruit-trade-dispute',
 'https://altoday.com/archives/23614-1st-appeals-court-to-weigh-donald-trumps-decision-to-end-daca',
 'https://altoday.com/archives/24222-donald-trump-tweet-takes-aim-at-jeff-sessions-again',
 'https://altoday.com/archives/23450-doug-jones-accepted-rosie-odonnell-campaign-donations-beyond-federal-legal-limit',
 'https://altoday.com/archives/21388-senate-bill-seeks-to-remove-anti-gay-language-from-states-sex-education-law',
 'https://altoday.com/archives/22992-terri-sewell-proposal-passes-in-irs-reform-package',
 'https://altoday.com/archives/24270-japans-prime-minister-to-meet-donald-trump-ahead-of-u-s-north-korea-summit',
 'https://altoday.com/archives/23109-how-the-media-blm-activists-are-pushing-false-narrative-of-chikesia-clemons-arrest-and-why-we-shouldnt-let-them',
 'https://altoday.com/archives/22450-trump-administration-sues-california-sales-us-land',
 'https://altoday.com/archives/23853-mike-pompeo-us-will-fight-russian-interference-in-2018-elections',
 'https://altoday.com/archives/24173-the-end-of-an-era-tea-party-class-of-house-republicans-fades',
 'https://altoday.com/archives/22622-state-appeals-abortion-ruling-minors-alabama',
 'https://altoday.com/archives/22182-last-gasp-try-immigration-deal-fell-partisan-disputes',
 'https://altoday.com/archives/22852-anxiety-grows-for-donald-trump-after-raid-on-his-personal-lawyer',
 'https://altoday.com/archives/22448-dc-officials-cite-gun-control-hypocrisy-condemning-marco-rubio',
 'https://altoday.com/archives/21451-ever-happened-spencer-bachus',
 'https://altoday.com/archives/23568-postal-service-more-financial-loss-as-mail-delivery-slumps',
 'https://altoday.com/archives/23066-after-close-vote-panel-sends-pompeo-nomination-to-senate',
 'https://altoday.com/archives/22071-alabama-gov-signs-first-tax-break-decade',
 'https://altoday.com/archives/23192-donald-trump-issues-disaster-declaration-for-ala-counties-following-delegation-letter',
 'https://altoday.com/archives/22630-governor-kay-ivey-needs-to-stop-john-coopers-bridge2nowhere',
 'https://altoday.com/archives/23214-kim-jong-un-says-hell-give-up-nukes-if-u-s-vows-not-to-attack',
 'https://altoday.com/archives/23121-terri-sewell-seeks-veteran-for-fellowship-in-birmingham-office',
 'https://altoday.com/archives/23175-house-panel-officially-clears-donald-trump-in-russia-probe',
 'https://altoday.com/archives/23843-donald-trump-eager-to-sign-bill-rolling-back-dodd-frank-regulations',
 'https://altoday.com/archives/23727-exclusive-true-story-of-waking-up-to-find-aldot-is-secretly-planning-to-build-a-fly-over-bridge-in-your-backyard',
 'https://altoday.com/archives/22559-kay-ivey-signs-ethics-exemption-law',
 'https://altoday.com/archives/23545-mo-brooks-calls-on-jeff-sessions-to-end-mueller-investigation-by-july-5',
 'https://altoday.com/archives/22205-richard-shelby-encourages-support-passage-of-60-billion-appropriations-bill',
 'https://altoday.com/archives/21582-dial',
 'https://altoday.com/archives/21727-russias-vladimir-putin-unveils-invincible-nuclear-weapons-mike-rogers-says-u-s-must-act',
 'https://altoday.com/archives/23565-chatter-grows-about-donald-trumps-nobel-peace-prize-prospects',
 'https://altoday.com/archives/22609-donald-trump-threatens-syria-strike-cancels-summit-travel',
 'https://altoday.com/archives/20731-talk-of-a-richard-shelby-censure-may-be-a-gop-turning-point',
 'https://altoday.com/archives/23133-ivey-leads-alabama-team-in-talks-with-japanese-automakers',
 'https://altoday.com/archives/22573-trump-era-transportation-project-focused-rural-areas-including-alabama',
 'https://altoday.com/archives/22975-justice-is-meant-to-be-blind',
 'https://altoday.com/archives/23840-alabama-mo-brooks-sue-over-inclusion-of-illegal-aliens-in-us-census',
 'https://altoday.com/archives/22060-state-senate-unanimously-approves-6-6-billion-education-budget',
 'https://altoday.com/archives/22120-first-lady-melania-trump-vows-fight-cyberbullying-despite-skeptics',
 'https://altoday.com/archives/21920-ethics-commission-director-says-bill-weakens-ethics-law',
 'https://altoday.com/archives/21895-fatal-school-shooting-reignites-alabama-legislative-debate']

def get_article(url):
#Sends request for url
    html = requests.get(url).text
    return html

def parse_article(html):
#BeautifulSoups the article
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h1', class_='post-title item fn').text
    body = soup.find('div', class_='post-content description').text

    article = {
        'title': title,
        'body': body,
        'source': 'Alabama Today',
        'num_source': 11
    }

    return article

def get_parsed_article_from_link(url):
#Runs the previous two functions on the url
    return parse_article(get_article(url))
#phase 1: uses request to try to BeautifulSoup links
al_list_o_articles = []
al_problem_articles = []
for text in al_first_articles:
    #print(text)
    try:
        art = get_parsed_article_from_link(text.encode())
        al_list_o_articles.append(art)

    except:
        print("Problem processing url " + text)
        problem = text
        al_problem_articles.append(problem)
    time.sleep(2)
#phase 2: uses selenium to go through links
driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
for x in al_problem_articles:
    try:
        driver.get(x)
        time.sleep(3)
        soupy = BeautifulSoup(driver.page_source, 'lxml')
        title = soupy.find('h1', class_='post-title item fn').text
        body = soupy.find('div').text

        articley = {
        'title': title,
        'body': body,
        'source': 'Alabama Today',
        'num_source': 11
        }
        al_list_o_articles.append(articley)
    except:
        pass
#Same as above but for expanded list, phase 1
al_more_list_o_articles = []
al_more_problem_articles = []
for text in al_more_articles:
    #print(text)
    try:
        art = get_parsed_article_from_link(text.encode())
        al_more_list_o_articles.append(art)

    except:
        print("Problem processing url " + text)
        problem = text
        al_more_problem_articles.append(problem)
    time.sleep(2)
driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
for x in al_more_problem_articles:
    try:
        driver.get(x)
        time.sleep(3)
        soupy = BeautifulSoup(driver.page_source, 'lxml')
        title = soupy.find('h1', class_='post-title item fn').text
        body = soupy.find('div').text

        articley = {
        'title': title,
        'body': body,
        'source': 'Alabama Today',
        'num_source': 11
        }
        al_more_list_o_articles.append(articley)
    except:
        pass
all_articles = al_list_o_articles + al_more_list_o_articles

#puts articles all into one list
all_articles = mj_list_o_articles + mj_more_list_o_articles
#starts client in Mongodb
client = MongoClient()
biased_news = client.project5.biased_news
#creates event and loads articles into Mongodb
db = client.events
biased_news = db.biased_news
biased_news.insert_many(all_articles)
