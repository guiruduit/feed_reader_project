# -*- coding: utf-8 -*-
# Project:
from models import Feader, Feed, UserProfile
# Django:
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Except:
from django.db import IntegrityError

def auto_login(request):
    post = request.POST
    username = post['username']
    password = post['password1']
    user = authenticate(username=username, password=password)
    if user.is_active:
        login(request, user)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.userprofile_set.create()
            auto_login(request)
            return HttpResponseRedirect('/lista_feeds/')
    else:
        form = UserCreationForm()
    return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def adiciona_feader(request):
    feader = None
    if Feader.objects.filter(url=request.POST['url_feader']):
        feader = Feader.objects.get(url__exact=request.POST['url_feader'])
#    try:
#        if Feader.objects.filter(url=request.POST['url_feader']):
#            feader = Feader.objects.get(url__exact=request.POST['url_feader'])
#    except:
#        feader = None
    if feader is not None:
        UserProfile.objects.get(user=request.user).feaders.add(feader)
        feader.refresh()
    else:
        UserProfile.objects.get(user=request.user).feaders.create(url=request.POST['url_feader'])
    return HttpResponseRedirect('/lista_feeds/')

@login_required
def lista_feeds(request, selected_feader=None):
    feaders = UserProfile.objects.get(user=request.user).feaders.all()
    if selected_feader:
        feeds = Feader.objects.get(pk=selected_feader).feed_set.all()
    else:
        feeds = []
        for feader in feaders:
            feeds.extend(feader.feed_set.all())

    excl_feeds = UserProfile.objects.get(user=request.user).excl_feeds.all()
    for excl_feed in excl_feeds:
        feeds.remove(excl_feed)

    return render_to_response('lista_feeds.html', {'feaders': feaders, 'feeds': feeds}, context_instance=RequestContext(request))

def refresh_feeds(request):
    feaders = UserProfile.objects.get(user=request.user).feaders.all()
    for feader in feaders:
        feader.refresh()
    return HttpResponseRedirect('/lista_feeds/')

def remove_feader(request, selected_feader):
    print selected_feader
    feader = Feader.objects.get(pk=selected_feader)
    UserProfile.objects.get(user=request.user).feaders.remove(feader)
    return HttpResponseRedirect('/lista_feeds/')

def remove_feed(request, selected_feed):
    feed = Feed.objects.get(pk=selected_feed)
    UserProfile.objects.get(user=request.user).excl_feeds.add(feed)
    return HttpResponseRedirect('/lista_feeds/')

def restore_excl_feeds(request):
    UserProfile.objects.get(user=request.user).excl_feeds.clear()
    return HttpResponseRedirect('/lista_feeds/')
