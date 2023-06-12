from django.views.generic import TemplateView, ListView, DetailView
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from repository import models
from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from collections import Counter
from repository.forms import BlogImport
import json
import base64
import requests
import random
import re
from django.utils.text import slugify
import mailchimp_marketing
from mailchimp_marketing.api_client import ApiClientError


def snippet_view(request, options):
    """
    create embeddable snippet page

    options:

    each

    use multiple tags to do AND

    'featured' - uses featured option rather than tag

    control options

    limit:2 - display 2
    related:slug - item slug, displays related items
    template:template name - referencs a embed_BLAH.html as the template


    e.g.

    /embed/fms/our-research/limit:2

    - two items in fms and our_research

    """

    limit = 4
    related_items = None
    template = "standard"
    related = False
    display_text = False
    render_json = False

    items = models.ResearchItem.objects.filter(published=True)

    for op in options.split("/"):
        if op:
            if ":" in op:
                option, value = op.split(":")
                if option == "limit":
                    limit = int(value)
                if option == "related":
                    related_items = value
                    related = True
                if option == "template":
                    template = value
                if option == "text":
                    if value.lower() in ["true", "t", "y", "yes"]:
                        display_text = True
                    else:
                        display_text = False
                if option == "format" and value == "json":
                    render_json = True
            else:
                if op == "featured":
                    featured_tags = models.Tag.objects.filter(featured=True)
                    featured_items = models.ResearchItem.objects.filter(
                        published=True, featured=True
                    )
                    items = list(featured_items) + list(featured_tags)
                else:
                    items = items.filter(tags__slug=op)

    if related_items:
        items = models.ResearchItem.objects.get(slug=related_items).similar_items(limit)
    else:
        if isinstance(items, list):
            items.sort(key=lambda x: x.date, reverse=True)
            items = items[:limit]
        else:
            items = items.distinct().order_by("-date")[:limit]

    if render_json:
        contents = [x.json() for x in items]
        return JsonResponse({"items": contents})

    context = {
        "items": items,
        "embed": True,
        "display_text": display_text,
        "related": related,
    }

    return render(request, "repository/embed_" + template + ".html", context)


class SitemapView(TemplateView):
    template_name = "sitemap.html"

    def get_context_data(self, **kwargs):
        context = super(SitemapView, self).get_context_data(**kwargs)
        context["site_base_url"] = settings.SITE_BASE_URL
        context["items"] = models.ResearchItem.objects.filter(published=True)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        return self.render_to_response(context, content_type="text/xml; charset=utf-8")


class ItemListView(ListView):
    model = models.ResearchItem
    context_object_name = "items"

    queryset = models.ResearchItem.objects.filter(published=True)


class ItemView(DetailView):
    model = models.ResearchItem
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super(ItemView, self).get_context_data(**kwargs)
        item = context["item"]

        json_ld_representation = {
            "@context": "http://schema.org",
            "@type": "ScholarlyArticle",
            "headline": item.title,
            "datePublished": item.date.isoformat(),
            "description": item.abstract.raw,
            "author": [],
            "url": item.absolute_url(),
        }

        if item.subtitle:
            json_ld_representation["alternativeHeadline"] = item.subtitle

        if item.thumbnail:
            json_ld_representation["image"] = (
                settings.SITE_BASE_URL + item.thumbnail.url
            )
        else:
            json_ld_representation["image"] = (
                settings.SITE_BASE_URL + "/static/img/report-thumbnail.png"
            )

        for author in item.author_list():

            json_ld_representation["author"].append(author.json_ld_representation())

        context["json_ld_representation"] = json.dumps(json_ld_representation)

        return context

    def get(self, request, *args, **kwargs):
        """
        Redirect to url if there is only one item with that slug
        """
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        # what I want is if there is one output, which is an URL, not a file,
        #  to redirect to that
        link_outputs = (
            context["item"]
            .outputs.exclude(Q(url__isnull=True) | Q(url__exact=""))
            .count()
        )

        if link_outputs == 1:
            return HttpResponseRedirect(context["item"].outputs.first().url)
        else:
            return self.render_to_response(context)


class PersonListView(ListView):
    model = models.Person
    context_object_name = "people"

    def get_queryset(self):
        return models.Person.objects.filter(list_in_people=True)


class PersonView(DetailView):
    model = models.Person
    context_object_name = "person"

    def get_context_data(self, **kwargs):
        context = super(PersonView, self).get_context_data(**kwargs)

        context["json_ld_representation"] = json.dumps(
            context["person"].json_ld_representation()
        )

        return context


class TagListView(ListView):
    model = models.TagGroup
    context_object_name = "taggroups"


class TagView(DetailView):
    model = models.Tag
    context_object_name = "tag"

    def get_context_data(self, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        top_tags = models.Tag.objects.filter(top_bar__gte=0)
        top_tags = list(top_tags.order_by("top_bar"))
        if context["tag"] not in top_tags:
            top_tags = []

        context["top_tags"] = top_tags
        return context

    def get_object(self, queryset=None):

        queryset = self.get_queryset()

        main_tag = queryset.filter(slug=self.kwargs["slug1"]).get()
        main_tag.selected_items = main_tag.get_research_items()
        filters = list(main_tag.display_filters.all().prefetch_related("tag"))
        main_tag.filters = []
        if filters:
            for d in filters:
                q = d.tag.get_research_items()
                q = q & main_tag.selected_items
                d.tag.count = q.count()

            filters.sort(key=lambda x: x.tag.count, reverse=True)
            filters.sort(key=lambda x: x.order)

            main_tag.filters = [x.tag for x in filters]

        main_tag.secondary_tag = None
        if "slug2" in self.kwargs:
            secondary_tag = queryset.filter(slug=self.kwargs["slug2"]).get()
            main_tag.secondary_tag = secondary_tag
        else:
            if main_tag.filters:
                main_tag.secondary_tag = main_tag.filters[0]

        if main_tag.secondary_tag:
            main_tag.display_items_in_years = (
                main_tag.secondary_tag.display_items_in_years
            )
            secondary_items = main_tag.secondary_tag.get_research_items()
            main_tag.selected_items = main_tag.selected_items & secondary_items
            if main_tag.secondary_tag not in main_tag.filters:
                main_tag.secondary_tag.count = main_tag.selected_items.count()
                main_tag.filters = [main_tag.secondary_tag] + main_tag.filters

        # group consecutive years with only one item
        main_tag.selected_items = list(main_tag.selected_items)
        main_tag.selected_items.sort(key=lambda x: x.date)

        count = Counter([x.date.year for x in main_tag.selected_items])

        for x, item in enumerate(main_tag.selected_items):
            item.grouped_year = str(item.date.year)
            if x == 0:
                continue
            prev = main_tag.selected_items[x - 1]
            prev_count = count[prev.date.year]
            current_count = count[item.date.year]
            if "-" not in prev.grouped_year:
                if prev_count + current_count == 2:
                    year = "{0} - {1}".format(prev.date.year, item.date.year)
                    prev.grouped_year = year
                    item.grouped_year = year

        # reverse chron
        main_tag.selected_items = main_tag.selected_items[::-1]

        return main_tag


def output_download(request, output_id):
    """
    update database and return actual url
    """
    item = models.ResearchOutput.objects.filter(id=output_id)
    if item.exists() is False:
        return HttpResponse("Download does not exist")
    item = item[0]
    item.increment_download()
    return HttpResponseRedirect(item.button_url())


def add_blog_based_on_social(request: HttpRequest):
    """
    Create a new entry based on a page in a blog. Require staff user
    """
    if not request.user.is_staff:
        return HttpResponse("Need to be staff user to use this feature.")
    new_url = None
    if request.method == "POST":
        form = BlogImport(request.POST)
        if form.is_valid():
            new_url = form.save()
    else:
        form = BlogImport()

    return render(
        request, "repository/blog_import.html", {"form": form, "new_url": new_url}
    )


def output_download_with_item_slug(request, item_slug, output_id):
    """
    Create special aliases for pdfs and full_text
    """
    if output_id not in ["pdf", "full_text"]:
        return output_download(request, output_id)

    item = models.ResearchItem.objects.get(slug=item_slug)
    urls = item.special_urls()
    output = urls.get(output_id, None)
    if output:
        return output_download(request, output.id)
    return HttpResponse("Missing {0} format".format(output_id))


def tracking_open_view(request):
    """
    View to return a tracking pixel and record the campaign information
    Expects a 'campaign' parameter in the query string.
    This stores opens at an aggregate campaign level and not individual level.
    """

    # get the campaign
    campaign_id = request.GET.get("campaign", "undefined")
    audience_id = request.GET.get("audience", "undefined")

    # when viewing the preview in mailchimp it looks like this
    if campaign_id == "*|CAMPAIGN_UID|*":
        return HttpResponse(
            base64.b64decode(
                b"R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
            ),
            content_type="image/gif",
        )

    # from the mailchimp api, get the campaign based on the unique id
    # from that, get the name of the campaign, and slugify it
    client = mailchimp_marketing.Client()
    client.set_config({"api_key": settings.MAILCHIMP_API_KEY, "server": "us9"})
    try:
        response = client.campaigns.get(campaign_id)
        campaign_name = response["settings"]["title"]
        campaign_slug = slugify(campaign_name)
        # if starts with auto, remove this
        if campaign_slug.startswith("auto"):
            campaign_slug = campaign_slug[5:]
    except ApiClientError as error:
        campaign_slug = campaign_id

    # config for the google analytics measurement api
    measurement_id = "G-2X56VXTG0K"
    api_secret = "1pSoMuDHTNi-wuHDf1n-fQ"

    # send event to be stored in google analytics
    send_event(
        measurement_id,
        api_secret,
        "email_open",
        {"campaign": campaign_slug, "audience": audience_id},
    )

    # return the pixel
    return HttpResponse(
        base64.b64decode(b"R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"),
        content_type="image/gif",
    )


def send_event(
    measurement_id: str, api_secret: str, event_name: str, event_params: dict[str, str]
):
    """
    Send an event to the google analytics measurement API
    """

    # create a random client_id, this is 2 32 bit integers seperated by a dot
    client_id = "{0}.{1}".format(
        random.randint(0, 2**32 - 1), random.randint(0, 2**32 - 1)
    )

    # check client id is in right format
    # it should be a string of two numbers seperated by a dot
    if not re.match(r"^\d+\.\d+$", client_id):
        raise Exception("client_id is not in the correct format")

    # if in debug mode, we need to add this to each event
    if settings.DEBUG:
        event_params["debug_mode"] = "1"

    # build payload
    payload = {
        "client_id": client_id,
        "events": [
            {
                "name": event_name,
                "params": event_params,
            }
        ],
    }

    # send payload
    url = "https://www.google-analytics.com/mp/collect"
    # this debug url gives clearer validation errors
    # url = "https://www.google-analytics.com/debug/mp/collect"
    headers = {
        "Content-Type": "application/json",
    }
    params = {
        "measurement_id": measurement_id,
        "api_secret": api_secret,
    }
    response = requests.post(
        url, headers=headers, params=params, data=json.dumps(payload)
    )
    if response.status_code not in [200, 204]:
        raise Exception(
            "Google Analytics Measurement Protocol API returned status code {}".format(
                response.status_code
            )
        )
