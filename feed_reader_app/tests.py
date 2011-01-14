# -*- coding: utf-8 -*-
# models tests:
from django.test import TestCase
# views tests:
from django.test.client import Client
from models import Feader
from views import lista_feeds

class TestAdicionaFeader(TestCase):

    client = None

    def setUp(self):
        self.client = Client()

    def test_adiciona_feader(self):
        tam = len(Feader.objects.all())
        response = self.client.post('/adiciona_feader/', {'url_feader': '__baguete'})
        self.failUnlessEqual(tam + 1, len(Feader.objects.all()))

class TestListaFeeds(TestCase):

    client = None
    response = None

    def setUp(self):
        baguete = Feader.objects.create(url="feed_reader_app/__baguete.xml")
        self.client = Client()

    def testa_lista_feeds(self):
        self.response = self.client.get('/', {})
        self.failUnlessEqual(200, self.response.status_code)

        # template
        self.failUnlessEqual(2, len(self.response.template))
        self.failUnlessEqual('lista_feeds.html', self.response.template[0].name)
        self.failUnlessEqual('base.html', self.response.template[1].name)

        # feaders
        self.failUnlessEqual(1, len(self.response.context['feaders']))
        self.failIfEqual('', self.response.context['feaders'][0]['title'])

        # feeds
        self.failUnlessEqual(20, len(self.response.context['feeds']))
        self.failIfEqual('', self.response.context['feeds'][0]['id'])
        self.failIfEqual('', self.response.context['feeds'][0]['title'])
        self.failIfEqual('', self.response.context['feeds'][0]['link'])
        self.failIfEqual('', self.response.context['feeds'][0]['date'])
        self.failIfEqual('', self.response.context['feeds'][0]['content'])

    def testa___quicksort(self):
        self.response = self.client.get('/', {})
        for index in range(len(self.response.context['feeds'])-1):
            self.failUnless(self.response.context['feeds'][index]['date'] >= self.response.context['feeds'][index+1]['date'])
