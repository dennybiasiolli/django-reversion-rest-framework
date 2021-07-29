from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from reversion.models import Version

from test_app.models import TestModel


class TestModelViewSetTests(APITestCase):
    def test_create_test_model(self):
        """
        Ensure we have history after creating a TestModel object.
        """
        url = reverse('testmodel-list')
        data = {'name': 'Foo 1.1.0'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('testmodel-history', kwargs={'pk': response.data['id']})
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertIsNotNone(response.data[0]['revision']['date_created'])
        self.assertIsNone(response.data[0]['revision']['user'])
        self.assertIsNotNone(response.data[0]['revision']['comment'])
        self.assertEqual(response.data[0]['field_dict']['name'], 'Foo 1.1.0')

    def test_editing_test_model(self):
        """
        Ensure we have history after editing a TestModel object.
        """
        url = reverse('testmodel-list')
        data = {'name': 'Foo 1.2.0'}
        response = self.client.post(url, data, format='json')

        url = reverse('testmodel-detail', kwargs={'pk': response.data['id']})
        data = {'name': 'Foo 1.2.1'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('testmodel-history', kwargs={'pk': response.data['id']})
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 2)
        self.assertIsNotNone(response.data[0]['revision']['date_created'])
        self.assertIsNone(response.data[0]['revision']['user'])
        self.assertIsNotNone(response.data[0]['revision']['comment'])
        self.assertEqual(response.data[0]['field_dict']['name'], 'Foo 1.2.1')
        self.assertIsNotNone(response.data[1]['revision']['date_created'])
        self.assertIsNone(response.data[1]['revision']['user'])
        self.assertIsNotNone(response.data[1]['revision']['comment'])
        self.assertEqual(response.data[1]['field_dict']['name'], 'Foo 1.2.0')

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

class TestModelsCustomSerializerViewSetTests(APITestCase):
    def test_create_test_model(self):
        """
        Ensure we have history after creating a TestModel object.
        """
        url = reverse('testmodelcustom-list')
        data = {'name': 'Foo 1.1.0'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('testmodelcustom-history', kwargs={'pk': response.data['id']})
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertIsNotNone(response.data[0]['revision']['date_created'])
        self.assertIsNone(response.data[0]['revision']['user'])
        self.assertIsNotNone(response.data[0]['revision']['comment'])
        self.assertEqual(response.data[0]['field_dict']['name'], 'Foo 1.1.0')

    def test_editing_test_model(self):
        """
        Ensure we have history after editing a TestModel object.
        """
        url = reverse('testmodelcustom-list')
        data = {'name': 'Foo 1.2.0'}
        response = self.client.post(url, data, format='json')

        url = reverse('testmodelcustom-detail', kwargs={'pk': response.data['id']})
        data = {'name': 'Foo 1.2.1'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('testmodelcustom-history', kwargs={'pk': response.data['id']})
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 2)
        self.assertIsNotNone(response.data[0]['revision']['date_created'])
        self.assertIsNone(response.data[0]['revision']['user'])
        self.assertIsNotNone(response.data[0]['revision']['comment'])
        self.assertEqual(response.data[0]['field_dict']['name'], 'Foo 1.2.1')
        self.assertIsNotNone(response.data[1]['revision']['date_created'])
        self.assertIsNone(response.data[1]['revision']['user'])
        self.assertIsNotNone(response.data[1]['revision']['comment'])
        self.assertEqual(response.data[1]['field_dict']['name'], 'Foo 1.2.0')

    def test_deleting_test_model(self):
        """
        Ensure we have deletion history after deleting a TestModel object.
        """
        url = reverse('testmodelcustom-list')
        data = {'name': 'Foo 1.2.0'}
        response = self.client.post(url, data, format='json')

        test_model_1 = TestModel.objects.get()
        url = reverse('testmodelcustom-detail', kwargs={'pk': test_model_1.pk})
        data = {'name': 'Foo 1.2.1'}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        versions_qs = Version.objects.get_deleted(TestModel)
        versions = versions_qs.filter(pk=test_model_1.pk)
        self.assertEqual(len(versions), 1)
