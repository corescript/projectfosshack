# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pprint
import time

# Create your views here.
import unirest
from django.http import HttpResponse
from django.shortcuts import render

from aylienapiclient import textapi

from .models import *


def index(request):
    queryset = news.objects.all()
    context = {
        'queryset':queryset,
    }
    return render(request,'index.html',context)

def get_news(request):


    response1 = unirest.get("https://newsapi.org/v1/articles/", headers={ "Accept": "application/json" }, params={"apiKey": "7a233aaececb44a3a0dd8576350c680e", "sortBy":"top", "source":"google-news"})

    articles = response1.body['articles']
    client = textapi.Client("faf883f4", "057f1bdde3dba11b14cf9abc9abbf986")
    for i in articles:
        data = news()
    	data.description = i['description']
        data.title = i['title']
        data.url = i['url']
        data.urlToImage = i['urlToImage']
        data.publishedAt = i['publishedAt']
        data.save()

        extract = client.Extract({"url": data.url, "best_image": True})
        atext = extract['article']

        #print extract
        """
        #try:
        response = unirest.post("https://api.aylien.com/api/v1/extract", headers={ "Accept": "application/json" }, params={ "text": data.url, "language": "en", "tab":"extract" })

        atext = response.body
        """
        print atext.rstrip()
        obj = article()
        obj.title = i['title']
        obj.text = atext.rstrip()

        emotion = unirest.post("http://apidemo.theysay.io/api/v1/emotion", headers={ "Accept": "application/json" }, params={ "text":obj.text, "level": "sentence" })
        print emotion['emotions'][0]

        topic = unirest.post("http://apidemo.theysay.io/api/v1/topic", headers={ "Accept": "application/json" }, params={ "text": obj.text, "level": "sentence" })
        print topic
        sentiment = unirest.post("http://apidemo.theysay.io/api/v1/sentiment", headers={ "Accept": "application/json" }, params={ "text": obj.text, "level": "sentence" })
        print sentiment
        obj.save()

        #except:
        #    print "Error :("
    #print place1

    return HttpResponse("DONE")


    #return render(request,'index.html',context=None)


def process_news(request):
    queryset = article.objects.all()


    emotion = unirest.post("http://apidemo.theysay.io/api/v1/emotion", headers={ "Accept": "application/json" }, params={ "text":"", "level": "sentence" })

    #print emotion.body
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(emotion.body)



    topic = unirest.post("http://apidemo.theysay.io/api/v1/topic", headers={ "Accept": "application/json" }, params={ "text": text, "level": "sentence" })

    #print topic.body
    pp.pprint(topic.body)

    sentiment = unirest.post("http://apidemo.theysay.io/api/v1/sentiment", headers={ "Accept": "application/json" }, params={ "text": text, "level": "sentence" })

    #print sentiment.body
    pp.pprint(sentiment.body)


def article_view(request,id=None):

    aobj =  article.objects.get(id=id)
    nobj = news.objects.get(title=aobj.title)
    context = {
        'aobj': aobj,
        'nobj': nobj,

    }
    return render(request,"article.html", context)
