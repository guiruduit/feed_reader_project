# -*- coding: utf-8 -*-
# Project:
from models import Feader
# Django:
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required
def adiciona_feader(request):
    if request.method == 'POST':
        post = request.POST
        if post['url_feader']:
            Feader.objects.create(url=post['url_feader'], user=request.user)
    return HttpResponseRedirect('/')

def __quicksort(vetor, campo):
    if campo == 'date':
        return __quicksort_by_date(vetor)
	if len(vetor) <= 1: return vetor
	middle = vetor[0][campo]
	return __quicksort([elemento for elemento in vetor if elemento[campo] > middle], campo) + \
		[elemento for elemento in vetor if elemento[campo] == middle] + \
		__quicksort([elemento for elemento in vetor if elemento[campo] < middle], campo)

def __quicksort_by_date(vetor):
    if len(vetor) <= 1:
        return vetor
    middle = vetor[0]['date']
    return __quicksort_by_date([elemento for elemento in vetor if __compare_datetimes(elemento['date'], middle) == 'greater']) + \
        [elemento for elemento in vetor if __compare_datetimes(elemento['date'], middle) == 'equal'] + \
        __quicksort_by_date([elemento for elemento in vetor if __compare_datetimes(elemento['date'], middle) == 'lower'])

def __compare_datetimes(date1, date2):
    if (date1.year > date2.year) \
        or (date1.month > date2.month) \
        or (date1.day > date2.day) \
        or (date1.hour > date2.hour) \
        or (date1.minute > date2.minute) \
        or (date1.second > date2.second):
        return 'greater'
    elif (date1.year == date2.year) \
        and (date1.month == date2.month) \
        and (date1.day == date2.day) \
        and (date1.hour == date2.hour) \
        and (date1.minute == date2.minute) \
        and (date1.second == date2.second):
        return 'equal'
    else:
        return 'lower'

@login_required
def lista_feeds(request):
    feaders = []
    feeds = []
    feaders_objects = Feader.objects.filter(user=request.user)
    for feader in feaders_objects:
        feaders.append(feader.get_feader_data())
        feeds = feeds + feader.get_feeds()
    __quicksort(feeds, 'date')
    return render_to_response('lista_feeds.html', {'feaders': feaders, 'feeds': feeds}, context_instance=RequestContext(request))
