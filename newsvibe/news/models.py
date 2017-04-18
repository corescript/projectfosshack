# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class news(models.Model):
	title = models.CharField(max_length = 300)
	description = models.TextField()
	url = models.URLField()
	urlToImage = models.URLField()
	publishedAt = models.CharField(max_length = 100)
