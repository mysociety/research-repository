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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from repository import views
from pages import views as pageViews

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^items/', views.ItemListView.as_view(), name='items'),
    url(r'^item/(?P<slug>[-\w]+)$', views.ItemView.as_view(), name='item'),

    url(r'^page/(?P<slug>[-\w]+)$', pageViews.PageView.as_view(), name='page'),

    url(r'^(?P<slug>[-\w]+)$', pageViews.PageView.as_view(), name='page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
