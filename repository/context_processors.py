from django.conf import settings
from pages.models import Page, Link
from repository.models import Tag

def get_pages_for_nav():
    pages = Page.objects.all().exclude(slug="home")
    pages = pages.exclude(nav_order=-1)
    pages = pages.order_by('nav_order')
    return pages

def add_settings( request ):
    """Add some selected settings values to the context"""
    return {
        'top_links':Link.objects.all().exclude(order=-1).order_by('order'),
        'all_pages':get_pages_for_nav(),
        'top_tags': Tag.objects.all().exclude(top_bar=-1).order_by('top_bar'),
        'settings': {
            'GOOGLE_ANALYTICS_ACCOUNT': settings.GOOGLE_ANALYTICS_ACCOUNT,
            'DEBUG': settings.DEBUG,
            'DEFAULT_SHARE_IMAGE': settings.DEFAULT_SHARE_IMAGE,
            'SITE_NAME': settings.SITE_NAME,
            'SITE_TWITTER_HANDLE': settings.SITE_TWITTER_HANDLE,            
            
        }
    }
