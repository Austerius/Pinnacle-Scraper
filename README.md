# Pinnacle-Scraper
Scrapping esport betting information from web site www.pinacle.com using Scrapy and Selenium. 

Take note: script was created for educational purposes to demonstrate usage of scrapy *Pipelines*,
*LinkExtractors*, "<i>Rules</i>", *Generic Spiders*, *Items*, *xpath selectors*.

So, what does this spider exactly doing(general <b>algorithm</b>):
1. Gather links to betting pages for each esport event(using appropriate set of rules).
2. Follow each extracted link and scrape esport data.
3. Filter gathered data in the pipeline.

After all processes finished we will get information about each single esport event to come. But, we <b>will
not include</b> events, that already passed(or in progress), and betting data for not primary events(such as betting
on "first blood", "second map winner" etc). Also, event/game time will be converted to <b>UTC</b> format. (If you want
include all events and keep original "site time" - comment code inside "<i>pipelines.py</i>" file or exclude pipelines
in "<i>setting.py</i>").

Keys and description for each returning line of information:
- '<i>date</i>'  - date of the single event/game in timedate format converted to UTC time(or tried to);
- '<i>game</i>' - name of the game(CS:GO, League of Legends, Dota 2 etc);
- '<i>player1</i>' - name of the first participant(or team name, like: "Fnatic" or "Team Liquid" etc);
- '<i>player2</i>' - name of the second participant;
- '<i>odds1</i>' - bet rate on the first player(float value, like: 1.862);
- '<i>odds2</i>' - bet rate on the second player(float value).

This script was written in Python 3.6(for scrapy 1.5) and tested on Windows machine. Before running it,
 you'll need to <b>install</b>:
- Scrapy (on Windows machine you'll need appropriate C++ SDK to run Twisted - check their docs);
- Selenium (with geckodriver for Windows machines);
- Firefox browser.

After installing all requirements - copy "<i>Pinnacle</i>" folder to your machine/device. Open "<i>pipelines.py</i>" file
and set variable "<b>TIME_DIFFERENCE</b>" to your own value (if needed).

To <b>run a spider</b> - change your location in terminal to scrapy project folder and type:</br> 
```scrapy crawl pinnacle```</br>
To save data to .json file(for example), type:</br> 
```scrapy crawl pinnacle -o yourfile.json```
