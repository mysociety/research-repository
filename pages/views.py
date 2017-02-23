from django.views.generic import DetailView

from pages import models


class PageView(DetailView):
    model = models.Page
    context_object_name = 'page'
