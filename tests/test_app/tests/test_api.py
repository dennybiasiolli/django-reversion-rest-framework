from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from reversion.models import Version

from test_app.models import TestModel


class TestModelTests(APITestCase):
    def test_create_test_model(self):
        """
        Ensure we have history after creating a TestModel object.
        """
        url = reverse('testmodel-list')
        data = {'name': 'Foo 1.1.0'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TestModel.objects.count(), 1)
        test_model_1 = TestModel.objects.get()
        self.assertEqual(test_model_1.name, 'Foo 1.1.0')
        versions = Version.objects.get_for_object(test_model_1)
        self.assertEqual(len(versions), 1)

    def test_editing_test_model(self):
        """
        Ensure we have history after editing a TestModel object.
        """
        url = reverse('testmodel-list')
        data = {'name': 'Foo 1.2.0'}
        response = self.client.post(url, data, format='json')

        test_model_1 = TestModel.objects.get()
        url = reverse('testmodel-detail', kwargs={'pk': test_model_1.pk})
        data = {'name': 'Foo 1.2.1'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        test_model_1 = TestModel.objects.get()
        self.assertEqual(test_model_1.name, 'Foo 1.2.1')
        versions = Version.objects.get_for_object(test_model_1)
        self.assertEqual(len(versions), 2)

    def test_deleting_test_model(self):
        """
        Ensure we have deletion history after deleting a TestModel object.
        """
        url = reverse('testmodel-list')
        data = {'name': 'Foo 1.2.0'}
        response = self.client.post(url, data, format='json')

        test_model_1 = TestModel.objects.get()
        url = reverse('testmodel-detail', kwargs={'pk': test_model_1.pk})
        data = {'name': 'Foo 1.2.1'}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        versions_qs = Version.objects.get_deleted(TestModel)
        versions = versions_qs.filter(pk=test_model_1.pk)
        self.assertEqual(len(versions), 1)
