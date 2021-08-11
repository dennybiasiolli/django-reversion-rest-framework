from rest_framework.viewsets import ModelViewSet
from .mixins import HistoryModelMixin

class HistoryModelViewSet(HistoryModelMixin, ModelViewSet):
    pass
