from django.views.generic import TemplateView, ListView, DetailView

from repository import models


class HomeView(TemplateView):
    template_name = 'index.html'


class ItemListView(ListView):
    model = models.ResearchItem
    context_object_name = 'items'


class ItemView(DetailView):
    model = models.ResearchItem
    context_object_name = 'item'
