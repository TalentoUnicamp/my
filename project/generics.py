from rest_framework.generics import GenericAPIView
from .mixins import PrefetchListModelMixin


class PrefetchListAPIView(PrefetchListModelMixin, GenericAPIView):
    """
    Concrete view for listing a queryset.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
