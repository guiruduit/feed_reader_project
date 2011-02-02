# -*- coding: utf-8 -*-
# python:
import feedparser
# models tests:
from django.test import TestCase
from django.contrib.auth.models import User
# views tests:
from django.test.client import Client
from models import Feader
from views import lista_feeds

class TestAdicionaFeader(TestCase):

    client = None
    user1 = None
    user2 = None
    baguete = None
    globo = None

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', email='user1@mail.com', password='1').userprofile_set.create()
        self.user2 = User.objects.create_user(username='user2', email='user2@mail.com', password='1').userprofile_set.create()
        self.baguete = feedparser.parse('feed_reader_app/__baguete.xml')
        self.globo = feedparser.parse('feed_reader_app/__globo.xml')

    def test_adiciona_feader(self):
        self.client.login(username='user1', password='1')
        tam = len(self.user1.feaders.all())
        response = self.client.post('/adiciona_feader/', {'url_feader': 'feed_reader_app/__baguete.xml'})
        self.failUnlessEqual(tam + 1, len(self.user1.feaders.all()))
        response = self.client.post('/adiciona_feader/', {'url_feader': 'feed_reader_app/__globo.xml'})
        self.failUnlessEqual(tam + 2, len(self.user1.feaders.all()))
        self.client.logout()

        tam2 = 0
        for feader in self.user1.feaders.all():
            tam2 += len(feader.feed_set.all())
        tam3 = len(self.baguete.entries) + len(self.globo.entries)
        self.failUnlessEqual(tam2, tam3)

        self.failUnlessEqual(2, len(Feader.objects.all()))

        self.client.login(username='user2', password='1')
        tam = len(self.user2.feaders.all())
        response = self.client.post('/adiciona_feader/', {'url_feader': 'feed_reader_app/__baguete.xml'})
        self.failUnlessEqual(tam + 1, len(self.user2.feaders.all()))

        self.failUnlessEqual(2, len(Feader.objects.all()))

class TestListaFeeds(TestCase):

    client = None
    response = None
    user = None

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='guilherme', email='gui@mail.com', password='1').userprofile_set.create()
        self.client.login(username='guilherme', password='1')
        baguete = Feader.objects.create(url='feed_reader_app/__baguete.xml')
        self.user.feaders.add(baguete)

    def testa_lista_feeds(self):
        self.response = self.client.get('/lista_feeds/', {})
        self.failUnlessEqual(200, self.response.status_code)

        # template
        self.failUnlessEqual(2, len(self.response.template))
        self.failUnlessEqual('lista_feeds.html', self.response.template[0].name)
        self.failUnlessEqual('base.html', self.response.template[1].name)

        # feaders
        self.failUnlessEqual(1, len(self.response.context['feaders']))
        feader = self.response.context['feaders'][0]
        self.failUnlessEqual("<class 'feed_reader_app.models.Feader'>", str(type(feader)))
        self.failIfEqual('', self.response.context['feaders'][0].title)

        # feeds
        self.failUnlessEqual(20, len(self.response.context['feeds']))
        self.failIfEqual('', self.response.context['feeds'][0].id)
        self.failIfEqual('', self.response.context['feeds'][0].title)
        self.failIfEqual('', self.response.context['feeds'][0].link)
        self.failIfEqual('', self.response.context['feeds'][0].date)
        self.failIfEqual('', self.response.context['feeds'][0].content)

        for feed in self.response.context['feeds']:
            self.failUnlessEqual(None, feed.validate_unique())

class TestRemoveFeader(TestCase):

    client = None
    response = None
    user1 = None
    user2 = None

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', email='user1@mail.com', password='1').userprofile_set.create()
        self.user2 = User.objects.create_user(username='user2', email='user2@mail.com', password='1').userprofile_set.create()

    def test_remove_feader(self):
        self.client.login(username='user1', password='1')
        response = self.client.post('/adiciona_feader/', {'url_feader': 'feed_reader_app/__baguete.xml'})
        response = self.client.post('/adiciona_feader/', {'url_feader': 'feed_reader_app/__globo.xml'})
        self.failUnlessEqual(2, len(self.user1.feaders.all()))

        feaders = Feader.objects.all()
        id_ = feaders[0].id

        tam_feaders_all = len(Feader.objects.all())
        response = self.client.post('/remove_feader/%d/' % id_)
        self.failUnlessEqual(tam_feaders_all - 1, len(self.user1.feaders.all()))
        self.failUnlessEqual(2, len(Feader.objects.all()))

class TestRemoveFeed(TestCase):

    client = None
    response = None
    user1 = None
    user2 = None

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', email='user1@mail.com', password='1').userprofile_set.create()
        self.user2 = User.objects.create_user(username='user2', email='user2@mail.com', password='1').userprofile_set.create()

    def test_remove_feed(self):
        self.client.login(username='user1', password='1')
        response = self.client.post('/adiciona_feader/', {'url_feader': 'feed_reader_app/__globo.xml'})

        feaders = Feader.objects.all()
        id_ = feaders[0].id

        feeds = []
        feeds.extend(self.user1.feaders.get(id=id_).feed_set.all())
        tam1 = len(feeds)

        id_ = feeds[0].id

        self.client.get('/remove_feed/%d/' % id_)
        excl_feeds = self.user1.excl_feeds.all()
        self.failUnlessEqual(1, len(excl_feeds))
        for excl_feed in excl_feeds:
            feeds.remove(excl_feed)
        self.failUnlessEqual(tam1 - 1, len(feeds))
