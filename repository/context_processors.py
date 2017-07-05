from django.conf import settings

def add_settings( request ):
    """Add some selected settings values to the context"""
    return {
        'settings': {
            'GOOGLE_ANALYTICS_ACCOUNT': settings.GOOGLE_ANALYTICS_ACCOUNT,
            'DEBUG': settings.DEBUG,
            'DEFAULT_SHARE_IMAGE': settings.DEFAULT_SHARE_IMAGE,
            'SITE_NAME': settings.SITE_NAME,
            'SITE_TWITTER_HANDLE': settings.SITE_TWITTER_HANDLE,            
            
        }
    }
