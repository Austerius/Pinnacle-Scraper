"""
This pipeline will do next:
- transform date of the single event to UTC format
- Drop all events/games that already passed
- Drop all events/games that not a primary(events, where you betting on 'first blood', '1st map winner' etc)

Enter your own value for :var:*TIME_DIFFERENCE*
"""
import datetime

from scrapy.exceptions import DropItem

# Its seems, all dates on site shows in -8 GMT zone(for me).
# Well, for now difference between UTC and site time:  -8 hour (but need to be monitor)
# Put your own value here, if it's different for you(with sight)
TIME_DIFFERENCE = -8


# just don't forgot to activate your pipeline settings
class PinnaclePipeline(object):

    def process_item(self, item, spider):

        # transforming string date to UTC datetime
        current_time_utc = datetime.datetime.utcnow()
        time_string = item['date']  # its looks like this: "Sat 03/02 15.15"
        first, second, third = time_string.split(" ")
        day, month = second.split("/")
        hour, minute = third.split(".")
        if (current_time_utc.month == 12) and (month < 11):  # its nor ok, but works for most part
            year = current_time_utc.year + 1
        else:
            year = current_time_utc.year
        site_time = datetime.datetime(year=year, month=int(month), day=int(day),
                                      hour=int(hour), minute=int(minute))
        game_time_utc = site_time - datetime.timedelta(minutes=TIME_DIFFERENCE*60)

        if current_time_utc > game_time_utc:
            raise DropItem("Event already passed or in progress")
        item['date'] = game_time_utc

        # Now selecting primary events:
        # not primary events have brackets '()' in players names: "Los Angeles Valiant (map 1)"
        if "(" in item['player1']:
            raise DropItem("Not a primary event: {}".format(item))
        if "select matches" in item['player1'].lower():
            raise DropItem("Not an event")

        return item
