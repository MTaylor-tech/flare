from django.db import models

import datetime
from django.utils import timezone
# Create your models here.

class LoreArticle(models.Model):
    article_slug = models.SlugField(blank=True)
    article_text = models.TextField(blank=True)
    article_title = models.CharField(max_length=100, blank=True)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.article_title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class LoreKeyword(models.Model):
    keyword_text = models.CharField(max_length=200)
    articles = models.ManyToManyField(LoreArticle)

    def __str__(self):
        return self.keyword_text
