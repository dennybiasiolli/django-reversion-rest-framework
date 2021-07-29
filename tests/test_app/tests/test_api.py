from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from test_app.models import TestModel


class TestModelTests(APITestCase):
    def test_create_test_model(self):
        """
        Ensure we have history after creating a TestModel object.
        """
        url = reverse('testmodel-list')
        data = {'name': 'Foo 1.0.0'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TestModel.objects.count(), 1)
        self.assertEqual(TestModel.objects.get().name, 'Foo 1.0.0')
