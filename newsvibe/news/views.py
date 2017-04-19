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
        try:
            data = news()
            data.description = i['description']
            data.title = i['title']
            data.url = i['url']
            data.urlToImage = i['urlToImage']
            data.publishedAt = i['publishedAt']
            

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
            sentiment = unirest.post("http://apidemo.theysay.io/api/v1/sentiment", headers={ "Accept": "application/json" }, params={ "text": obj.text, "level": "sentence" })
            try:    
                '''
                obj.calm = emotion.body[0]['emotions'][1]['score']
                obj.fear = emotion.body[0]['emotions'][2]['score']
                obj.happy = emotion.body[0]['emotions'][3]['score']
                obj.like = emotion.body[0]['emotions'][4]['score']
                obj.shame = emotion.body[0]['emotions'][5]['score']
                obj.sure = emotion.body[0]['emotions'][6]['score']
                obj.surprise = emotion.body[0]['emotions'][7]['score']
                topic = unirest.post("http://apidemo.theysay.io/api/v1/topic", headers={ "Accept": "application/json" }, params={ "text": obj.text, "level": "sentence" })
                top_3 = []
                try:    
                    top_3[0] =  topic.body[0]['scores'][0]['label']
                    top_3[1] = topic.body[0]['scores'][1]['label']
                    top_3[2] = topic.body[0]['scores'][2]['label']
                except:
                    pass
                print top_3
                obj.negative =  sentiment.body[0]['sentiment']['negative']
                obj.positive =  sentiment.body[0]['sentiment']['positive']
                obj.neutral =  sentiment.body[0]['sentiment']['neutral']
                obj.label =  sentiment.body[0]['sentiment']['label']
                obj.anger = emotion.body[0]['emotions'][0]['score']
                obj.save()
                '''
               
                topic = unirest.post("http://apidemo.theysay.io/api/v1/topic", headers={ "Accept": "application/json" }, params={ "text": obj.text, "level": "sentence" })
                top_3 = []
                try:    
                    top_3[0] =  topic.body[0]['scores'][0]['label']
                    top_3[1] = topic.body[0]['scores'][1]['label']
                    top_3[2] = topic.body[0]['scores'][2]['label']
                except:
                    pass
                print top_3
                data.positive =  sentiment.body[0]['sentiment']['positive']
                data.label =  sentiment.body[0]['sentiment']['label']
                data.negative =  sentiment.body[0]['sentiment']['negative']
                
                data.neutral =  sentiment.body[0]['sentiment']['neutral']
                
                data.calm = emotion.body[0]['emotions'][1]['score']
                data.fear = emotion.body[0]['emotions'][2]['score']
                data.happy = emotion.body[0]['emotions'][3]['score']
                data.like = emotion.body[0]['emotions'][4]['score']
                data.shame = emotion.body[0]['emotions'][5]['score']
                data.sure = emotion.body[0]['emotions'][6]['score']
                data.surprise = emotion.body[0]['emotions'][7]['score']

                data.anger = emotion.body[0]['emotions'][0]['score']
                obj.save()

            except:
                pass
            #except:
            #    print "Error :("
    #print place1
            data.save()
        except:
            pass
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


def article_view(request,slug=None):
    nobj = news.objects.get(slug=slug)
    aobj =  article.objects.get(title=nobj.title)
   
    
    #aobj =  article.objects.get(slug=slug)
    #nobj = news.objects.get(title=aobj.title)
    context = {
        'aobj': aobj,
        'nobj': nobj,

    }
    return render(request,"article.html", context)
