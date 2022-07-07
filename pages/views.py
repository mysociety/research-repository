from django.views.generic import DetailView, TemplateView

from pages import models
from repository import models as repository_models
from django.http.response import HttpResponse
import feedparser
import datetime


class FeedCache(object):
    """
    basic cacher for imported rss feed
    """

    _feed = []
    _time = None
    feed_url = "https://www.mysociety.org/category/research/feed"
    timeout = 15 * 60

    @classmethod
    def is_time(cls):
        if cls._time == None:
            return True
        else:
            return datetime.datetime.now() > cls._time + datetime.timedelta(
                seconds=cls.timeout
            )

    @classmethod
    def fetch_feed(cls):
        if cls.is_time():
            cls._feed = feedparser.parse(cls.feed_url)
            cls._time = datetime.datetime.now()

        for e in cls._feed["entries"][:5]:
            yield e["title"], e["link"]


class HomeView(TemplateView):
    template_name = "pages/home_page.html"

    def get_context_data(self, **kwargs):

        context = super(TemplateView, self).get_context_data(**kwargs)

        context["feed"] = FeedCache.fetch_feed()
        context["page"] = models.Page.objects.get_or_create(slug="home")[0]

        featured_items = repository_models.ResearchItem.objects.filter(
            published=True, featured=True
        )

        featured_tags = repository_models.Tag.objects.filter(featured=True)
        featured = list(featured_items) + list(featured_tags)

        featured.sort(key=lambda x: x.date, reverse=True)

        context["featured_items"] = featured

        return context


class PageView(DetailView):
    model = models.Page
    context_object_name = "page"


def opt_out_view(request, experiment, user_id):
    allowed_experiments = ["ps1"]
    if experiment in allowed_experiments:
        model, created = models.OptOut.objects.get_or_create(
            experiment=experiment, user_id=user_id
        )
        return HttpResponse(
            "ID {0} opted-out. Contact research@mysociety.org with further questions.".format(
                user_id
            )
        )
    else:
        return HttpResponse(
            "{0} is not a registered experiment. Contact research@mysociety.org".format(
                experiment
            )
        )
