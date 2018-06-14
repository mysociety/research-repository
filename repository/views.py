from django.views.generic import TemplateView, ListView, DetailView
from django.conf import settings
from django.http import HttpResponseRedirect
from repository import models
from django.shortcuts import render
from django.db.models import Q

import json

def snippet_view(request,options):
    """
    create embeddable snippet page
    
    options:
    
    seperate OR slugs with /
    require AND slugs with +
    
    control options
    
    limit:2 - display 2
    related:slug - item slug, displays related items
    template:template name - referencs a embed_BLAH.html as the template
    
    
    """
    
    limit = 100
    related_items = None
    template = 'standard'
    
    master = Q()
    
    for op in options.split("/"):
        if ":" in op:
            option, value = op.split(":")
            if option == "limit":
                limit = value
            if option == "related":
                related_items = value
            if option == "template":
                template = value
        else:
            q = Q()
            for o in op.split("+"):
                q &= Q(tags__slug=o)
            master |= q
    
    if related_items:
        items = models.ResearchItem.objects.get(slug=related_items).similar_items()[:limit]
    else:
        items = models.ResearchItem.objects.filter(master).filter(published=True)
        items = items.distinct().order_by('-date')[:limit]
    
    context = {'items':items}
    
    return render(request, 'repository/embed_' + template + ".html", context) 

class SitemapView(TemplateView):
    template_name = 'sitemap.html'

    def get_context_data(self, **kwargs):
        context = super(SitemapView, self).get_context_data(**kwargs)
        context['site_base_url'] = settings.SITE_BASE_URL
        context['items'] = models.ResearchItem.objects.filter(published=True)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        return self.render_to_response(context, content_type="text/xml; charset=utf-8")


class ItemListView(ListView):
    model = models.ResearchItem
    context_object_name = 'items'

    queryset = models.ResearchItem.objects.filter(published=True)


class ItemView(DetailView):
    model = models.ResearchItem
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super(ItemView, self).get_context_data(**kwargs)
        item = context['item']

        json_ld_representation = {
                "@context": "http://schema.org",
                "@type": "ScholarlyArticle",
                "headline": item.title,
                "datePublished": item.date.isoformat(),
                "description": item.abstract.raw,
                "author": [],
                "url": item.absolute_url()
            }

        if item.subtitle:
            json_ld_representation['alternativeHeadline'] = item.subtitle

        if item.thumbnail:
            json_ld_representation['image'] = settings.SITE_BASE_URL + item.thumbnail.url
        else:
            json_ld_representation['image'] = settings.SITE_BASE_URL + '/static/img/report-thumbnail.png'

        for author in item.author_list():

            json_ld_representation['author'].append(author.json_ld_representation())

        context['json_ld_representation'] = json.dumps(json_ld_representation)

        return context


class PersonListView(ListView):
    model = models.Person
    context_object_name = 'people'

    def get_queryset(self):
        return models.Person.objects.filter(list_in_people=True)


class PersonView(DetailView):
    model = models.Person
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        context = super(PersonView, self).get_context_data(**kwargs)

        context['json_ld_representation'] = json.dumps(context['person'].json_ld_representation())

        return context


class TagListView(ListView):
    model = models.TagGroup
    context_object_name = 'taggroups'


class TagView(DetailView):
    model = models.Tag
    context_object_name = 'tag'


def output_download(request,output_id):
    """
    update database and return actual url
    """
    item = models.ResearchOutput.objects.get(id=output_id)
    item.increment_download()
    return HttpResponseRedirect(item.button_url())

