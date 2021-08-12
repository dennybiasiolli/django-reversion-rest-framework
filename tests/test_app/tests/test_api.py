from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from test_app.models import TestModel


class AuthApiTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.user1 = User.objects.create_user(
            'user1', 'user1@email.it', 'password')
        self.user2 = User.objects.create_user(
            'user2', 'user2@email.it', 'password')
        self.client.login(username='user1', password='password')


class TestModelViewSetTests(AuthApiTestCase):
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
        self.assertIsNotNone(response.data[0]['id'])
        self.assertIsNotNone(response.data[0]['revision']['date_created'])
        self.assertEqual(response.data[0]['revision']['user'], 1)
        self.assertIsNotNone(response.data[0]['revision']['comment'])
        self.assertEqual(response.data[0]['field_dict']['name'], 'Foo 1.1.0')

    def test_editing_test_model(self):
        """
        Ensure we have history after editing a TestModel object.
        """
        url = reverse('testmodel-list')
        data = {'name': 'Foo 1.2.0'}
        response = self.client.post(url, data, format='json')

        self.client.login(username='user2', password='password')
        url = reverse('testmodel-detail', kwargs={'pk': response.data['id']})
        data = {'name': 'Foo 1.2.1'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('testmodel-history', kwargs={'pk': response.data['id']})
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 2)
        self.assertIsNotNone(response.data[0]['id'])
        self.assertIsNotNone(response.data[0]['revision']['date_created'])
        self.assertEqual(response.data[0]['revision']['user'], 2)
        self.assertIsNotNone(response.data[0]['revision']['comment'])
        self.assertEqual(response.data[0]['field_dict']['name'], 'Foo 1.2.1')
        self.assertIsNotNone(response.data[1]['id'])
        self.assertIsNotNone(response.data[1]['revision']['date_created'])
        self.assertEqual(response.data[1]['revision']['user'], 1)
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
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse('testmodel-deleted')
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertIsNotNone(response.data[0]['id'])
        self.assertIsNotNone(response.data[0]['revision']['date_created'])
        self.assertEqual(response.data[0]['revision']['user'], 1)
        self.assertIsNotNone(response.data[0]['revision']['comment'])
        self.assertEqual(response.data[0]['field_dict']['id'], test_model_1.pk)
        self.assertEqual(response.data[0]['field_dict']['name'], 'Foo 1.2.0')


class TestModelsCustomSerializerViewSetTests(AuthApiTestCase):
    def test_create_test_model(self):
        """
        Ensure we have history after creating a TestModel object.
        """
        url = reverse('testmodelcustom-list')
        data = {'name': 'Foo 1.1.0'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('testmodelcustom-history',
                      kwargs={'pk': response.data['id']})
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertIsNotNone(response.data[0]['id'])
        self.assertIsNotNone(response.data[0]['revision']['date_created'])
        self.assertEqual(response.data[0]['revision']['user']['id'], 1)
        self.assertEqual(response.data[0]['revision']['user']['username'], 'user1')
        self.assertIsNotNone(response.data[0]['revision']['comment'])
        self.assertEqual(response.data[0]['field_dict']['name'], 'Foo 1.1.0')

    def test_editing_test_model(self):
        """
        Ensure we have history after editing a TestModel object.
        """
        url = reverse('testmodelcustom-list')
        data = {'name': 'Foo 1.2.0'}
        response = self.client.post(url, data, format='json')

        self.client.login(username='user2', password='password')
        url = reverse('testmodelcustom-detail',
                      kwargs={'pk': response.data['id']})
        data = {'name': 'Foo 1.2.1'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('testmodelcustom-history',
                      kwargs={'pk': response.data['id']})
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 2)
        self.assertIsNotNone(response.data[0]['id'])
        self.assertIsNotNone(response.data[0]['revision']['date_created'])
        self.assertEqual(response.data[0]['revision']['user']['id'], 2)
        self.assertEqual(response.data[0]['revision']['user']['username'], 'user2')
        self.assertIsNotNone(response.data[0]['revision']['comment'])
        self.assertEqual(response.data[0]['field_dict']['name'], 'Foo 1.2.1')
        self.assertIsNotNone(response.data[1]['id'])
        self.assertIsNotNone(response.data[1]['revision']['date_created'])
        self.assertEqual(response.data[1]['revision']['user']['id'], 1)
        self.assertEqual(response.data[1]['revision']['user']['username'], 'user1')
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
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse('testmodelcustom-deleted')
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertIsNotNone(response.data[0]['id'])
        self.assertIsNotNone(response.data[0]['revision']['date_created'])
        self.assertEqual(response.data[0]['revision']['user']['id'], 1)
        self.assertEqual(response.data[0]['revision']['user']['username'], 'user1')
        self.assertIsNotNone(response.data[0]['revision']['comment'])
        self.assertEqual(response.data[0]['field_dict']['id'], test_model_1.pk)
        self.assertEqual(response.data[0]['field_dict']['name'], 'Foo 1.2.0')
