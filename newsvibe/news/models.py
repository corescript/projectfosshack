# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class news(models.Model):
	title = models.CharField(max_length = 300,default="Not available")
	description = models.TextField(default="Not available")
	url = models.URLField(default="Not available")
	urlToImage = models.URLField(default="Not available")
	publishedAt = models.CharField(max_length = 100,default="Not available")
