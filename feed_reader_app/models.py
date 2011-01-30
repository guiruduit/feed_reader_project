# -*- coding: utf-8 -*-
# Django:
from django.db import models
from django.contrib.auth.models import User
# Python:
import feedparser
from datetime import datetime
# Except:
from django.db import IntegrityError, DatabaseError

class Feader(models.Model):

    """
    >>> baguete = Feader.objects.create(url="feed_reader_app/__baguete.xml")
    >>> type (baguete)
    <class 'feed_reader_app.models.Feader'>
    >>> baguete.id == baguete.pk
    True
    >>> print baguete.title[0:7]
    Baguete

    >>> feeds = baguete.feed_set.all()
    >>> len(feeds) < 100
    True
    >>> len(feeds)
    20
    >>> f = feeds[0]
    >>> type(f)
    <class 'feed_reader_app.models.Feed'>
    >>> f.feader == baguete
    True
    >>> print f.title
    Braspress: R$ 33 mi para renovar TI com Oracle
    >>> f.delete()

    >>> feeds2 = baguete.feed_set.all()
    >>> len(feeds2)
    19

    >>> u = User.objects.create(username='u', password='1').userprofile_set.create()
    >>> type(u)
    <class 'feed_reader_app.models.UserProfile'>
    >>> u.feaders.add(baguete)
    >>> len(u.feaders.all())
    1
    """

    url = models.CharField('URL Feader', max_length=200)
    title = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.title

    __feader_xml = None

    def __parse_feader_xml(self):
        if not self.__feader_xml:
            self.__feader_xml = feedparser.parse(self.url)

    def save(self, *args, **kwargs):
        self.__parse_feader_xml()
        self.title = self.__feader_xml['channel']['title']
        super(Feader, self).save(*args, **kwargs)
        self.__save_feeds()

    def get_absolute_url(self):
        return '/lista_feeds/%i' % self.id

    def __save_feeds(self):
        for feed_xml in self.__feader_xml.entries[0:100]:
            title = feed_xml['title']
            link = feed_xml['link']
            content = feed_xml['description']
            date = self.__convert_parseddate_to_datetime(feed_xml['date_parsed'])
            if not Feed.objects.filter(link=link):
                Feed.objects.create(title=title, link=link, date=date, content=content, feader=self)
#            try:
#                Feed.objects.create(title=title, link=link, date=date, content=content, feader=self)
#            except (IntegrityError, DatabaseError):
#                pass

    def refresh(self):
        self.__parse_feader_xml()
        self.__save_feeds()

    def __convert_parseddate_to_datetime(self, parseddate):
        return datetime(parseddate.tm_year, parseddate.tm_mon, parseddate.tm_mday, parseddate.tm_hour, parseddate.tm_min, parseddate.tm_sec)

class Feed(models.Model):

#    class Meta:
#        unique_together = ('title', 'link', 'date', 'content', 'feader')

    title = models.CharField(max_length=200)
    link = models.URLField(verify_exists=False, unique=True)
    date = models.DateTimeField()
    content = models.TextField()
    feader = models.ForeignKey(Feader)

    def __unicode__(self):
        return self.title

class UserProfile(models.Model):

    user = models.ForeignKey(User, unique=True, blank=False)
    feaders = models.ManyToManyField(Feader)

    def __unicode__(self):
        return self.user.username
