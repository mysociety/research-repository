"""repository URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from repository import views
from pages import views as pageViews
from django.views.generic import RedirectView
admin.autodiscover()

urlpatterns = [

    url(r'^$', pageViews.HomeView.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
    url('^api/', include('repository.api_views')),
    url(r'^sitemap\.xml$', views.SitemapView.as_view(), name='sitemap'),
    url(r'^publications/outputs/(?P<output_id>[-\w]+$)', views.output_download, name='download'),
    url(r'^publications/(?P<item_slug>[-\w]+)/outputs/(?P<output_id>[-\w]+$)', views.output_download_with_item_slug, name='download_special'),
    url(r'^publications/(?P<slug>[-\w]+)$', views.ItemView.as_view(), name='item'),
    url(r'^publications/', views.ItemListView.as_view(), name='items'),

    url(r'^research/outputs/(?P<output_id>[-\w]+$)', RedirectView.as_view(pattern_name='download', permanent=True)),
    url(r'^research/(?P<slug>[-\w]+)$', RedirectView.as_view(pattern_name='item', permanent=True)),
    url(r'^research/', RedirectView.as_view(pattern_name='items', permanent=True)),

    url(r'^people/(?P<slug>[-\w]+)$', views.PersonView.as_view(), name='person'),
    url(r'^people/', views.PersonListView.as_view(), name='people'),

    url(r'^section/(?P<slug1>[-\w]+)/(?P<slug2>[-\w]+)$', views.TagView.as_view(), name='tag'),
    url(r'^section/(?P<slug1>[-\w]+)$', views.TagView.as_view(), name='tag'),
    url(r'^tag/(?P<slug>[-\w]+)$', RedirectView.as_view(pattern_name='tag', permanent=True)),
    url(r'^tags/', views.TagListView.as_view(), name='tags'),
    url(r'^embed/(?P<options>.+)', views.snippet_view, name='embed'),
    url(r'^optout/(?P<experiment>[-\w]+)/(?P<user_id>[-\w]+)$', pageViews.opt_out_view, name='page'),
    url(r'^(?P<slug>[-\w]+)$', pageViews.PageView.as_view(), name='page'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
