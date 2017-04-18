# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
import unirest

def get_news(request):
	

    response1 = unirest.get("https://newsapi.org/v1/articles/", headers={ "Accept": "application/json" }, params={"apiKey": "7a233aaececb44a3a0dd8576350c680e", "sortBy":"top", "source":"google-news"})
    
    articles = response1.body['articles']
    
    for i in articles:
    	print i['author']
    #print place1 
    
    return HttpResponse("DONE")
   

    #return render(request,'index.html',context=None)
