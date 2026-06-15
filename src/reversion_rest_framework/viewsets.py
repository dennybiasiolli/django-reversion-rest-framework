from rest_framework.viewsets import ModelViewSet

from .mixins import RestoreMixin, RevertMixin


class HistoryModelViewSet(RevertMixin, RestoreMixin, ModelViewSet):
    pass
