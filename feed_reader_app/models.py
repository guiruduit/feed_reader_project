# -*- coding: utf-8 -*-
# Django:
from django.db import models
# Python:
import feedparser
from datetime import datetime

class Feader(models.Model):
    """
    # get_feader_data():
    >>> baguete = Feader.objects.create(url="feed_reader_app/__baguete.xml")
    >>> b = baguete.get_feader_data()
    >>> b['title']
    u"Baguete - \\xdaltimas not\\xedcias"
    >>> b['link']
    u"http://www.baguete.com.br/noticias"

    # get_feeds():
    >>> baguete_feeds = baguete.get_feeds(10)
    >>> len(baguete_feeds)
    10
    >>> first_feed = baguete_feeds[0]
    >>> len(first_feed)
    5
    >>> first_feed['id']
    1
    >>> first_feed['title']
    u'Gartner: BI m\\xf3vel e para todos'
    >>> first_feed['link']
    u'http://www.baguete.com.br/noticias/software/12/01/2011/gartner-bi-movel-e-para-todos'
    >>> first_feed['content'][0:100]
    u'<p>\\n\\tOs aplicativos de Business Inteligence dever&atilde;o ganhar cada vez mais espa&ccedil;o nos di'

    # __convert_parseddate_to_datetime():
    >>> print first_feed['date']
    2011-01-12 11:56:24
    """
    url = models.CharField(max_length=200)

    feader_xml = ''

    def get_feader_data(self):
        if not self.feader_xml:
            self.feader_xml = feedparser.parse(self.url)
        return {'title': self.feader_xml['channel']['title'], 'link': self.feader_xml['channel']['link']}

    def get_feeds(self, number_of_feeds=20):
        feeds = []
        feed_id = 0
        if not self.feader_xml:
            self.feader_xml = feedparser.parse(self.url)
        for feed_xml in self.feader_xml.entries if len(self.feader_xml.entries) <= number_of_feeds else self.feader_xml.entries[0:number_of_feeds]:
            feeds.append({
                'id': feed_id + 1,
                'title': feed_xml['title'],
                'link': feed_xml['link'],
                'date': self.__convert_parseddate_to_datetime(feed_xml['date_parsed']),
                'content': feed_xml['description']
            })
        return feeds

    def __convert_parseddate_to_datetime(self, parseddate):
        return datetime(parseddate.tm_year, parseddate.tm_mon, parseddate.tm_mday, parseddate.tm_hour, parseddate.tm_min, parseddate.tm_sec)
