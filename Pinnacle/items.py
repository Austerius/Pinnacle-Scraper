import scrapy


class Event(scrapy.Item):
    game = scrapy.Field()
    date = scrapy.Field()
    player1 = scrapy.Field()
    odds1 = scrapy.Field()
    player2 = scrapy.Field()
    odds2 = scrapy.Field()
