# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')




from time import sleep
from lxml import html     # it is used to parse requested pages with xpath expressions for scraping
import csv,os,json        # these module are used to create files for outputting our data
from exceptions import ValueError   #  this will handle errors when an error code is sent for a page request
from time import sleep# this will be used to wait some seconds without embarking on an activity / task
import datetime#  its a module for recording time
import requests, sys, webbrowser, bs4          # requests,bs4,webbrowser : for scraping webpages
from bs4 import BeautifulSoup
import time
from lxml import html



from django.shortcuts import render

# Create your views here.

from .models import Book, Author, BookInstance, Genre


def index(request):

    titles = []
    hrefs = []

    cho = 1
    toprint = []

    if request.GET.get('cat'):

        cat = request.GET.get('cat')

        search_params = "+".join((request.GET.get('terms')).split(" "))

        if int(cat) == 1:
            url = 'https://www.lowes.com/search?searchTerm=' + search_params + '&catalog=4294395604'
        else:
            url = 'https://www.lowes.com/search?searchTerm=' + search_params + '&catalog=4294418688'

        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36'})

        if page.status_code!=200:
            raise ValueError('captha')

        sleep(0.1)  # the sleeps are so as not to overwhelm a website with many requests ; this leads to a ConnectionError

        htmx = page.content
        htmx = htmx.encode('utf-8', 'ignore')
        soup = BeautifulSoup(htmx, "lxml")


        toprint.append("PRODUCTS FROM LOWE'S ::")
        toprint.append("--------------------")

        for link in soup.find_all("a", class_="display-block"):
            if cho<16:
                title = ((link.get_text()).encode('utf-8')).strip(" ")
                href = link.get('href')
                
                if not len(href)<6:
                    title = title.replace("\n", "")
                    title = title.replace("  ", "")  
                    titles.append(str(cho)+".  "+str(title))
                    hrefs.append(href)
                    cho = cho+1
            else:
                pass

    return render(request, 'index.html',{
        #'cat': search,
        #'terms': name,
        'cat': toprint,
        'terms': titles,
    })