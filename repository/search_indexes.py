from haystack import indexes

from .models import SearchItem


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True, use_template=True, template_name="search_text_index.txt"
    )
    title = indexes.CharField()

    def get_model(self):
        return SearchItem

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(research_item__published=True)
