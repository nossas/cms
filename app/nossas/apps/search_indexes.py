from datetime import datetime
from haystack import indexes
from .models import Campaign


class CampaignIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr="release_date")

    def get_model(self):
        return Campaign

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().on_site.filter(release_date__lte=datetime.now())
