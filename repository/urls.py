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
    1. Import the include() function: from django.urls import include, re_path, path, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView

from haystack.forms import SearchForm
from haystack.views import SearchView

from pages import views as pageViews
from repository import views

admin.autodiscover()

urlpatterns = [
    path("", pageViews.HomeView.as_view(), name="home"),
    re_path(r"^email/open/", views.tracking_open_view, name="open_view"),
    re_path(r"^admin/", admin.site.urls),
    path("api/", include("repository.api_views")),
    re_path(r"^sitemap\.xml$", views.SitemapView.as_view(), name="sitemap"),
    re_path(
        r"^publications/outputs/(?P<output_id>[-\w]+$)",
        views.output_download,
        name="download",
    ),
    re_path(
        r"^publications/(?P<item_slug>[-\w]+)/outputs/(?P<output_id>[-\w]+$)",
        views.output_download_with_item_slug,
        name="download_special",
    ),
    re_path(r"^publications/(?P<slug>[-\w]+)$", views.ItemView.as_view(), name="item"),
    re_path(r"^publications/", views.ItemListView.as_view(), name="items"),
    re_path(
        r"^research/outputs/(?P<output_id>[-\w]+$)",
        RedirectView.as_view(pattern_name="download", permanent=True),
    ),
    re_path(
        r"^research/(?P<slug>[-\w]+)$",
        RedirectView.as_view(pattern_name="item", permanent=True),
    ),
    re_path(r"^research/", RedirectView.as_view(pattern_name="items", permanent=True)),
    re_path(r"^people/(?P<slug>[-\w]+)$", views.PersonView.as_view(), name="person"),
    re_path(r"^people/", views.PersonListView.as_view(), name="people"),
    re_path(
        r"^section/(?P<slug1>[-\w]+)/(?P<slug2>[-\w]+)$",
        views.TagView.as_view(),
        name="tag",
    ),
    re_path(r"^section/(?P<slug1>[-\w]+)$", views.TagView.as_view(), name="tag"),
    re_path(
        r"^tag/(?P<slug>[-\w]+)$",
        RedirectView.as_view(pattern_name="tag", permanent=True),
    ),
    re_path(r"^import_blog", views.add_blog_based_on_social, name="import_blog"),
    re_path(r"^tags/", views.TagListView.as_view(), name="tags"),
    re_path(r"^embed/(?P<options>.+)", views.snippet_view, name="embed"),
    re_path(
        r"^optout/(?P<experiment>[-\w]+)/(?P<user_id>[-\w]+)$",
        pageViews.opt_out_view,
        name="page",
    ),
    re_path(r"^(?P<slug>[-\w]+)$", pageViews.PageView.as_view(), name="page"),
    path("markitup/", include("markitup.urls")),
    re_path(
        r"^search/",
        SearchView(form_class=SearchForm),
    ),
    # url(r"^search/", views.ResearchSearchView.as_view(), name="search_view"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
