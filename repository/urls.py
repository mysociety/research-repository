"""URL configuration for the research repository."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from haystack.forms import SearchForm
from haystack.views import SearchView

from pages import views as pageViews
from repository import views

admin.autodiscover()

urlpatterns = [
    path("", pageViews.HomeView.as_view(), name="home"),
    path("email/open/", views.tracking_open_view, name="open_view"),
    path("admin/", admin.site.urls),
    path("api/", include("repository.api_views")),
    path("sitemap.xml", views.SitemapView.as_view(), name="sitemap"),
    path(
        "publications/outputs/<int:output_id>",
        views.output_download,
        name="download",
    ),
    path(
        "publications/<slug:item_slug>/outputs/<slug:output_id>",
        views.output_download_with_item_slug,
        name="download_special",
    ),
    path("publications/<slug:slug>", views.ItemView.as_view(), name="item"),
    path("publications/", views.ItemListView.as_view(), name="items"),
    path(
        "research/outputs/<int:output_id>",
        RedirectView.as_view(pattern_name="download", permanent=True),
    ),
    path(
        "research/<slug:slug>",
        RedirectView.as_view(pattern_name="item", permanent=True),
    ),
    path("research/", RedirectView.as_view(pattern_name="items", permanent=True)),
    path("people/<slug:slug>", views.PersonView.as_view(), name="person"),
    path("people/", views.PersonListView.as_view(), name="people"),
    path(
        "section/<slug:slug1>/<slug:slug2>",
        views.TagView.as_view(),
        name="tag",
    ),
    path("section/<slug:slug1>", views.TagView.as_view(), name="tag"),
    path(
        "tag/<slug:slug>",
        RedirectView.as_view(pattern_name="tag", permanent=True),
    ),
    path("import_blog", views.add_blog_based_on_social, name="import_blog"),
    path("tags/", views.TagListView.as_view(), name="tags"),
    path("embed/<path:options>", views.snippet_view, name="embed"),
    path(
        "optout/<slug:experiment>/<slug:user_id>",
        pageViews.opt_out_view,
        name="page",
    ),
    path("<slug:slug>", pageViews.PageView.as_view(), name="page"),
    path("markitup/", include("markitup.urls")),
    path(
        "search/",
        SearchView(form_class=SearchForm),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
