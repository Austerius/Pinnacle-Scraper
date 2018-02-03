"""
This scrapy spider will scrape betting data about esports events from web site "pinnacle.com"

Take note: script was created for educational purposes to demonstrate usage of scrapy *Pipelines*,
*LinkExtractors*, "Rules", *Generic Spiders*, *Items*, *xpath selectors*.

So, what does this spider exactly doing(general algorithm):
    1. Gather links to betting pages for each esport event(using appropriate set of rules).
    2. Follow each extracted link and scrape esport data.
    3. Filter gathered data in the pipeline.
After all processes finished we will get information about each single esport event to come. But, we will
not include events, that already passed(or in progress), and betting data for not primary events(such as betting
on "first blood", "second map winner" etc). Also, event/game time will be converted to UTC format. (If you want
include all events and keep original "site time" - comment code inside "pipelines.py" file or exclude pipelines
in "setting.py").

Keys and description for each returning line of information:
- 'date'  - date of the single event/game in timedate format converted to UTC time(or tried to);
- 'game' - name of the game(CS:GO, League of Legends, Dota 2 etc);
- 'player1' - name of the first participant(or team name, like: "Fnatic" or "Team Liquid" etc);
- 'player2' - name of the second participant;
- 'odds1' - bet rate on the first player(float value, like: 1.862);
- 'odds2' - bet rate on the second player(float value).

This script was written in Python 3.6(for scrapy 1.5) and tested on Windows machine. Before running it,
 you'll need to install:
- Scrapy (on Windows machine you'll need appropriate C++ SDK to run Twisted - check their docs);
- Selenium (with geckodriver for Windows machines);
- Firefox browser.
After installing all requirements - copy "Pinnacle" folder to your machine/device. Open "pipelines.py" file
and set variable "TIME_DIFFERENCE" to your own value (if needed).

To run a spider - change your location in terminal to scrapy project folder and type: scrapy crawl pinnacle
To save data to .json file(for example), type: scrapy crawl pinnacle -o yourfile.json
"""

import time

from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy import Selector
from Pinnacle.items import Event

from selenium import webdriver


class Pinnacle(CrawlSpider):
    """
    Spider for extracting links, following them and parsing data from response.
    Note: we using here a generic scrapy spider "CrawlSpider" (instead of "scrapy.Spider")
    and set of rules to extract only "required" urls.
    """

    name = 'pinnacle'
    allowed_domains = ["www.pinnacle.com"]
    start_urls = ["https://www.pinnacle.com/en/"]
    # Our esport events always have this part in their links: "odds/match/e-sports/"
    rules = (
        Rule(LxmlLinkExtractor(allow="odds/match/e-sports/",
                               allow_domains=allowed_domains,
                               restrict_css="ul li.level-2", unique=True), callback='parse_item'),
            )

    def load_page(self, url, sleeptime):
        """Load page with selenium and get source code after page fully loaded"""
        driver = webdriver.Firefox()
        driver.get(url)
        time.sleep(sleeptime)
        source = Selector(text=driver.page_source)
        driver.close()
        return source

    def parse_item(self, response):
        sleeptime = 2
        game_name = response.xpath('//header//div[@class="breadcrumbs"]/a[3]/text()').extract_first()
        # ok, for 'New Market' category we need to get game name from another place
        if game_name == "New Markets":
            # we get something like this "eSports CS:GO - GOTV.GG Invitational Odds"
            game_name = response.xpath('//h1[@class="sport-title"]/text()').extract_first()
            # take 2nd word from previous string
            game_name = game_name.split(" ")[1]

        # getting dynamically loaded content:
        source = self.load_page(response.url, sleeptime)
        # Now we going to find all tables with events on current page and loop through them
        events_table = source.xpath('//div[@ng-repeat="date in currentPeriod.dates"]')
        for table in events_table:
            item = Event()
            # getting all rows in current table and loop through them(don't forget relative '.' in xpath):
            rows = table.xpath('.//table[@class="odds-data"]//tbody')
            date_string = table.xpath('.//div[@class="toolbar"]//span[2]/text()').extract_first()
            for row in rows:
                time_string = row.xpath('.//tr[1]//td[@class="game-time ng-scope"]//span/text()').extract_first()
                site_date_string = date_string + time_string

                player1 = row.xpath('.//tr[1]//td[@class="game-name name"]//span/text()').extract_first()
                odds1 = row.xpath('.//tr[1]//td[@class="oddTip game-moneyline"]//span/text()').extract_first()
                try:
                    odds1 = float(odds1.strip())
                except:
                    pass

                player2 = row.xpath('.//tr[2]//td[@class="game-name name"]//span/text()').extract_first()
                odds2 = row.xpath('.//tr[2]//td[@class="oddTip game-moneyline"]//span/text()').extract_first()
                try:
                    odds2 = float(odds2.strip())
                except:
                    pass

                item['game'] = game_name
                item['date'] = site_date_string
                item['player1'] = player1
                item['odds1'] = odds1
                item['player2'] = player2
                item['odds2'] = odds2
                yield item
