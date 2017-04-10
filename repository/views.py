from django.views.generic import TemplateView, ListView, DetailView
from django.conf import settings

from repository import models

import json


class SitemapView(TemplateView):
    template_name = 'sitemap.html'

    def get_context_data(self, **kwargs):
        context = super(SitemapView, self).get_context_data(**kwargs)
        context['site_base_url'] = settings.SITE_BASE_URL
        context['items'] = models.ResearchItem.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        return self.render_to_response(context, content_type="text/xml; charset=utf-8")


class ItemListView(ListView):
    model = models.ResearchItem
    context_object_name = 'items'


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

        for author in item.author_list():
            author_representation = {
                    "@type": "Person",
                    "familyName": author.last_name,
                    "givenName": author.first_name,
                    "name": author.full_name(),
                    "sameAs": []
                }

            if author.institution:
                author_representation['affiliation'] = {
                        "@type": "Organization",
                        "name": author.institution,
                    }

            if author.url:
                author_representation['url'] = author.url
                author_representation['sameAs'].append(author.url)

            if author.orcid:
                author_representation['sameAs'].append('http://orcid.org/' + author.orcid)

            if author.researcherid:
                author_representation['sameAs'].append('http://www.researcherid.com/rid/' + author.researcherid)

            if author.twitter:
                author_representation['sameAs'].append('https://twitter.com/' + author.twitter)

            json_ld_representation['author'].append(author_representation)

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
