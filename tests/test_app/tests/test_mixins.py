from django.test.testcases import TestCase
from rest_framework.viewsets import GenericViewSet
from reversion_rest_framework import mixins
from reversion_rest_framework.serializers import VersionSerializer


class MixinsTests(TestCase):
    def test_base_history_model_mixin(self):
        """
        Ensure we don't have actions but only version_serializer
        """
        class TestViewSet(mixins.BaseHistoryModelMixin, GenericViewSet):
            pass

        url_paths = list(
            action.url_path for action in TestViewSet.get_extra_actions()
        )
        self.assertEqual(len(url_paths), 0)
        self.assertEqual(TestViewSet.version_serializer, VersionSerializer)

    def test_history_only_mixin(self):
        """
        Ensure we have only the history action
        """
        class TestViewSet(mixins.HistoryOnlyMixin, GenericViewSet):
            pass

        url_paths = list(
            action.url_path for action in TestViewSet.get_extra_actions()
        )
        self.assertTrue(
            issubclass(mixins.HistoryOnlyMixin, mixins.BaseHistoryModelMixin))
        self.assertEqual(len(url_paths), 2)
        self.assertTrue('history' in url_paths)
        self.assertTrue(r'history/(?P<version_pk>\d+)' in url_paths)

    def test_deleted_only_mixin(self):
        """
        Ensure we have only the deleted action
        """
        class TestViewSet(mixins.DeletedOnlyMixin, GenericViewSet):
            pass

        url_paths = list(
            action.url_path for action in TestViewSet.get_extra_actions()
        )
        self.assertTrue(
            issubclass(mixins.DeletedOnlyMixin, mixins.BaseHistoryModelMixin))
        self.assertIsNone(TestViewSet.version_model)
        self.assertEqual(len(url_paths), 1)
        self.assertTrue('deleted' in url_paths)

    def test_read_only_history_model_mixin(self):
        """
        Ensure we have history and deleted actions
        """
        class TestViewSet(mixins.ReadOnlyHistoryModel, GenericViewSet):
            pass

        url_paths = list(
            action.url_path for action in TestViewSet.get_extra_actions()
        )
        self.assertTrue(
            issubclass(mixins.ReadOnlyHistoryModel, mixins.HistoryOnlyMixin))
        self.assertTrue(
            issubclass(mixins.ReadOnlyHistoryModel, mixins.DeletedOnlyMixin))
        self.assertEqual(len(url_paths), 3)
        self.assertTrue('history' in url_paths)
        self.assertTrue('deleted' in url_paths)

    def test_revert_mixin(self):
        """
        Ensure we have revert action
        """
        class TestViewSet(mixins.RevertMixin, GenericViewSet):
            pass

        url_paths = list(
            action.url_path for action in TestViewSet.get_extra_actions()
        )
        self.assertTrue(
            issubclass(mixins.RevertMixin, mixins.HistoryOnlyMixin))
        self.assertEqual(len(url_paths), 3)
        self.assertTrue('history' in url_paths)
        self.assertTrue(r'history/(?P<version_pk>\d+)' in url_paths)
        self.assertTrue(r'revert/(?P<version_pk>\d+)' in url_paths)

    def test_history_model_mixin(self):
        """
        Ensure we have all actions
        """
        class TestViewSet(mixins.HistoryModelMixin, GenericViewSet):
            pass

        url_paths = list(
            action.url_path for action in TestViewSet.get_extra_actions()
        )
        self.assertTrue(
            issubclass(mixins.HistoryModelMixin, mixins.RevertMixin))
        self.assertTrue(
            issubclass(mixins.HistoryModelMixin, mixins.DeletedOnlyMixin))
        self.assertEqual(len(url_paths), 4)
        self.assertTrue('history' in url_paths)
        self.assertTrue(r'history/(?P<version_pk>\d+)' in url_paths)
        self.assertTrue(r'revert/(?P<version_pk>\d+)' in url_paths)
        self.assertTrue('deleted' in url_paths)
