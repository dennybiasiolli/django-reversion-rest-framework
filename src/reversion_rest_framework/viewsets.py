from rest_framework.viewsets import ModelViewSet

from .mixins import DeletedMixin, RevertMixin


class HistoryModelViewSet(RevertMixin, DeletedMixin, ModelViewSet):
    pass
