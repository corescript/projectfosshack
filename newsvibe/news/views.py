# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.
import unirest

def index(request):
	
    return render(request,'index.html',context=None)

def get_news(request):
	

    response1 = unirest.get("https://newsapi.org/v1/articles/", headers={ "Accept": "application/json" }, params={"apiKey": "7a233aaececb44a3a0dd8576350c680e", "sortBy":"top", "source":"google-news"})
    
    articles = response1.body['articles']
    
    for i in articles:
        data = news()
    	data.description = i['description']
        data.title = i['title']
        data.url = i['url']
        data.urlToImage = i['urlToImage']
        data.publishedAt = i['publishedAt']
        data.save()
    #print place1 
    
    return HttpResponse("DONE")
   

    #return render(request,'index.html',context=None)
