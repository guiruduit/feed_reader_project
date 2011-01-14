# -*- coding: utf-8 -*-
# models tests:
from django.test import TestCase
# views tests:
from django.test.client import Client
from models import Feader
from django.contrib.auth.models import User
from views import lista_feeds

class TestAdicionaFeader(TestCase):

    client = None
    user = None

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='guilherme', email='gui@mail.com', password='1')
        self.client.login(username='guilherme', password='1')

    def test_adiciona_feader(self):
        tam = len(Feader.objects.filter(user=self.user))
        response = self.client.post('/adiciona_feader/', {'url_feader': '__baguete'})
        self.failUnlessEqual(tam + 1, len(Feader.objects.filter(user=self.user)))

class TestListaFeeds(TestCase):

    client = None
    response = None
    user = None

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='guilherme', email='gui@mail.com', password='1')
        self.client.login(username='guilherme', password='1')
        baguete = Feader.objects.create(url="feed_reader_app/__baguete.xml", user=self.user)

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
