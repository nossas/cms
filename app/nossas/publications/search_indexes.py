from datetime import datetime
from haystack import indexes
from .models import Publication


class PublicationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr="updated_at")

    def get_model(self):
        return Publication

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().on_site.filter(updated_at__lte=datetime.now())
