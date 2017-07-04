from django.views.generic import DetailView, TemplateView

from pages import models
from repository import models as page_models

import feedparser
import datetime

class FeedCache(object):
    """
    basic cacher for imported rss feed
    """
    _feed = []
    _time = None
    feed_url = "https://www.mysociety.org/category/research/feed"
    timeout = 15*60
    
    @classmethod
    def is_time(cls):
        if cls._time == None:
            return True
        else:
            return datetime.datetime.now() > cls._time + datetime.timedelta(seconds=cls.timeout)
    
    @classmethod
    def fetch_feed(cls):
        if cls.is_time():
            cls._feed = feedparser.parse(cls.feed_url)
            cls._time = datetime.datetime.now()
        
        for e in cls._feed["entries"][:5]:
            yield e["title"],e["link"]


class HomeView(TemplateView):
    template_name = "pages//home_page.html"
    
    def get_context_data(self,**kwargs):
        
        return {'feed':FeedCache.fetch_feed(),
                'publications':page_models.ResearchItem.objects.all().order_by('-date')[:5],
                'page':models.Page.objects.get_or_create(slug="home")[0]
                }
        

class PageView(DetailView):
    model = models.Page
    context_object_name = 'page'
