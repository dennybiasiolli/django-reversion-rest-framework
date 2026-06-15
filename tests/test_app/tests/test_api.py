import string

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.test import APITestCase
from test_app.models import TestLimitedModel, TestModel


class AuthApiTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        User = get_user_model()
        self.user1 = User.objects.create_user("user1", "user1@email.it", "password")
        self.user2 = User.objects.create_user("user2", "user2@email.it", "password")
        self.client.login(username="user1", password="password")


class TestModelViewSetTests(AuthApiTestCase):
    def test_create_test_model(self):
        """
        Ensure we have history after creating a TestModel object.
        """
        url = reverse("testmodel-list")
        data = {"name": "Foo 1.1.0"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse("testmodel-history", kwargs={"pk": response.data["id"]})
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 1)
        self.assertIsNotNone(response.data[0]["id"])
        self.assertIsNotNone(response.data[0]["revision"]["date_created"])
        self.assertEqual(response.data[0]["revision"]["user"], 1)
        self.assertIsNotNone(response.data[0]["revision"]["comment"])
        self.assertEqual(response.data[0]["field_dict"]["name"], "Foo 1.1.0")

    def test_editing_test_model(self):
        """
        Ensure we have history after editing a TestModel object.
        """
        url = reverse("testmodel-list")
        data = {"name": "Foo 1.2.0"}
        response = self.client.post(url, data, format="json")

        self.client.login(username="user2", password="password")
        url = reverse("testmodel-detail", kwargs={"pk": response.data["id"]})
        data = {"name": "Foo 1.2.1"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse("testmodel-history", kwargs={"pk": response.data["id"]})
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 2)
        self.assertIsNotNone(response.data[0]["id"])
        self.assertIsNotNone(response.data[0]["revision"]["date_created"])
        self.assertEqual(response.data[0]["revision"]["user"], 2)
        self.assertIsNotNone(response.data[0]["revision"]["comment"])
        self.assertEqual(response.data[0]["field_dict"]["name"], "Foo 1.2.1")
        self.assertIsNotNone(response.data[1]["id"])
        self.assertIsNotNone(response.data[1]["revision"]["date_created"])
        self.assertEqual(response.data[1]["revision"]["user"], 1)
        self.assertIsNotNone(response.data[1]["revision"]["comment"])
        self.assertEqual(response.data[1]["field_dict"]["name"], "Foo 1.2.0")

    def test_deleting_test_model(self):
        """
        Ensure we have deletion history after deleting a TestModel object.
        """
        url = reverse("testmodel-list")
        data = {"name": "Foo 1.2.0"}
        response = self.client.post(url, data, format="json")

        test_model_1 = TestModel.objects.get()
        url = reverse("testmodel-detail", kwargs={"pk": test_model_1.pk})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse("testmodel-deleted")
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 1)
        self.assertIsNotNone(response.data[0]["id"])
        self.assertIsNotNone(response.data[0]["revision"]["date_created"])
        self.assertEqual(response.data[0]["revision"]["user"], 1)
        self.assertIsNotNone(response.data[0]["revision"]["comment"])
        self.assertNotIn("id", response.data[0]["field_dict"])
        self.assertEqual(response.data[0]["field_dict"]["name"], "Foo 1.2.0")

    def test_reverting_test_model(self):
        """
        Ensure we have history after reverting a TestModel object.
        """
        url = reverse("testmodel-list")
        data = {"name": "Foo 1.2.0"}
        response = self.client.post(url, data, format="json")

        self.client.login(username="user2", password="password")
        url = reverse("testmodel-detail", kwargs={"pk": response.data["id"]})
        data = {"name": "Foo 1.2.1"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        pk = response.data["id"]
        url = reverse("testmodel-history", kwargs={"pk": pk})
        response = self.client.get(url, format="json")

        url = reverse(
            "testmodel-revert",
            kwargs={
                "pk": pk,
                "version_pk": response.data[1]["id"],
            },
        )
        response = self.client.post(url, data, format="json")
        self.assertIsNotNone(response.data["id"])
        self.assertIsNotNone(response.data["revision"]["date_created"])
        self.assertEqual(response.data["revision"]["user"], 1)
        self.assertIsNotNone(response.data["revision"]["comment"])
        self.assertEqual(response.data["field_dict"]["name"], "Foo 1.2.0")

        url = reverse("testmodel-history", kwargs={"pk": pk})
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 3)
        self.assertIsNotNone(response.data[0]["id"])
        self.assertIsNotNone(response.data[0]["revision"]["date_created"])
        self.assertEqual(response.data[0]["revision"]["user"], 2)
        self.assertIsNotNone(response.data[0]["revision"]["comment"])
        self.assertEqual(response.data[0]["field_dict"]["name"], "Foo 1.2.0")
        self.assertIsNotNone(response.data[1]["id"])
        self.assertIsNotNone(response.data[1]["revision"]["date_created"])
        self.assertEqual(response.data[1]["revision"]["user"], 2)
        self.assertIsNotNone(response.data[1]["revision"]["comment"])
        self.assertEqual(response.data[1]["field_dict"]["name"], "Foo 1.2.1")
        self.assertIsNotNone(response.data[2]["id"])
        self.assertIsNotNone(response.data[2]["revision"]["date_created"])
        self.assertEqual(response.data[2]["revision"]["user"], 1)
        self.assertIsNotNone(response.data[2]["revision"]["comment"])
        self.assertEqual(response.data[2]["field_dict"]["name"], "Foo 1.2.0")


class TestModelsCustomSerializerViewSetTests(AuthApiTestCase):
    def test_create_test_model(self):
        """
        Ensure we have history after creating a TestModel object.
        """
        url = reverse("testmodelcustom-list")
        data = {"name": "Foo 1.1.0"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse("testmodelcustom-history", kwargs={"pk": response.data["id"]})
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 1)
        self.assertIsNotNone(response.data[0]["id"])
        self.assertIsNotNone(response.data[0]["revision"]["date_created"])
        self.assertEqual(response.data[0]["revision"]["user"]["id"], 1)
        self.assertEqual(response.data[0]["revision"]["user"]["username"], "user1")
        self.assertIsNotNone(response.data[0]["revision"]["comment"])
        self.assertEqual(response.data[0]["field_dict"]["name"], "Foo 1.1.0")

    def test_editing_test_model(self):
        """
        Ensure we have history after editing a TestModel object.
        """
        url = reverse("testmodelcustom-list")
        data = {"name": "Foo 1.2.0"}
        response = self.client.post(url, data, format="json")

        self.client.login(username="user2", password="password")
        url = reverse("testmodelcustom-detail", kwargs={"pk": response.data["id"]})
        data = {"name": "Foo 1.2.1"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse("testmodelcustom-history", kwargs={"pk": response.data["id"]})
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 2)
        self.assertIsNotNone(response.data[0]["id"])
        self.assertIsNotNone(response.data[0]["revision"]["date_created"])
        self.assertEqual(response.data[0]["revision"]["user"]["id"], 2)
        self.assertEqual(response.data[0]["revision"]["user"]["username"], "user2")
        self.assertIsNotNone(response.data[0]["revision"]["comment"])
        self.assertEqual(response.data[0]["field_dict"]["name"], "Foo 1.2.1")
        self.assertIsNotNone(response.data[1]["id"])
        self.assertIsNotNone(response.data[1]["revision"]["date_created"])
        self.assertEqual(response.data[1]["revision"]["user"]["id"], 1)
        self.assertEqual(response.data[1]["revision"]["user"]["username"], "user1")
        self.assertIsNotNone(response.data[1]["revision"]["comment"])
        self.assertEqual(response.data[1]["field_dict"]["name"], "Foo 1.2.0")

    def test_deleting_test_model(self):
        """
        Ensure we have deletion history after deleting a TestModel object.
        """
        url = reverse("testmodelcustom-list")
        data = {"name": "Foo 1.2.0"}
        response = self.client.post(url, data, format="json")

        test_model_1 = TestModel.objects.get()
        url = reverse("testmodelcustom-detail", kwargs={"pk": test_model_1.pk})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse("testmodelcustom-deleted")
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 1)
        self.assertIsNotNone(response.data[0]["id"])
        self.assertIsNotNone(response.data[0]["revision"]["date_created"])
        self.assertEqual(response.data[0]["revision"]["user"]["id"], 1)
        self.assertEqual(response.data[0]["revision"]["user"]["username"], "user1")
        self.assertIsNotNone(response.data[0]["revision"]["comment"])
        self.assertNotIn("id", response.data[0]["field_dict"])
        self.assertEqual(response.data[0]["field_dict"]["name"], "Foo 1.2.0")

    def test_reverting_test_model(self):
        """
        Ensure we have history after reverting a TestModel object.
        """
        url = reverse("testmodelcustom-list")
        data = {"name": "Foo 1.2.0"}
        response = self.client.post(url, data, format="json")

        self.client.login(username="user2", password="password")
        url = reverse("testmodelcustom-detail", kwargs={"pk": response.data["id"]})
        data = {"name": "Foo 1.2.1"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        pk = response.data["id"]
        url = reverse("testmodelcustom-history", kwargs={"pk": pk})
        response = self.client.get(url, format="json")

        url = reverse(
            "testmodelcustom-revert",
            kwargs={
                "pk": pk,
                "version_pk": response.data[1]["id"],
            },
        )
        response = self.client.post(url, data, format="json")
        self.assertIsNotNone(response.data["id"])
        self.assertIsNotNone(response.data["revision"]["date_created"])
        self.assertEqual(response.data["revision"]["user"]["id"], 1)
        self.assertEqual(response.data["revision"]["user"]["username"], "user1")
        self.assertIsNotNone(response.data["revision"]["comment"])
        self.assertEqual(response.data["field_dict"]["name"], "Foo 1.2.0")

        url = reverse("testmodelcustom-history", kwargs={"pk": pk})
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 3)
        self.assertIsNotNone(response.data[0]["id"])
        self.assertIsNotNone(response.data[0]["revision"]["date_created"])
        self.assertEqual(response.data[0]["revision"]["user"]["id"], 2)
        self.assertEqual(response.data[0]["revision"]["user"]["username"], "user2")
        self.assertIsNotNone(response.data[0]["revision"]["comment"])
        self.assertEqual(response.data[0]["field_dict"]["name"], "Foo 1.2.0")
        self.assertIsNotNone(response.data[1]["id"])
        self.assertIsNotNone(response.data[1]["revision"]["date_created"])
        self.assertEqual(response.data[1]["revision"]["user"]["id"], 2)
        self.assertEqual(response.data[1]["revision"]["user"]["username"], "user2")
        self.assertIsNotNone(response.data[1]["revision"]["comment"])
        self.assertEqual(response.data[1]["field_dict"]["name"], "Foo 1.2.1")
        self.assertIsNotNone(response.data[2]["id"])
        self.assertIsNotNone(response.data[2]["revision"]["date_created"])
        self.assertEqual(response.data[2]["revision"]["user"]["id"], 1)
        self.assertEqual(response.data[2]["revision"]["user"]["username"], "user1")
        self.assertIsNotNone(response.data[2]["revision"]["comment"])
        self.assertEqual(response.data[2]["field_dict"]["name"], "Foo 1.2.0")


class TestModelsPaginatedViewSetTests(AuthApiTestCase):
    """
    Ensure that the pagination works as expected,
    and that individual revisions can be obtained.
    """

    def test_pagination_history(self):
        create_url = reverse("testmodelpaginated-list")

        response = self.client.post(create_url, {"name": "Foo 1.2.0"}, format="json")
        pk = response.data["id"]

        update_url = reverse(
            "testmodelpaginated-detail", kwargs={"pk": response.data["id"]}
        )

        for letter in string.ascii_lowercase:
            self.client.patch(update_url, {"name": letter}, format="json")

        history_base_url = reverse("testmodelpaginated-history", kwargs={"pk": pk})
        for page, count in [(1, 10), (2, 10), (3, 7)]:
            query_kwargs = {"page": page}
            history_url = f"{history_base_url}?{urlencode(query_kwargs)}"
            response = self.client.get(history_url, format="json")
            self.assertEqual(response.data["count"], 27)
            self.assertEqual(len(response.data["results"]), count)

        for version_pk, name in enumerate(string.ascii_lowercase, start=2):
            historic_version_url = reverse(
                "testmodelpaginated-version",
                kwargs={"pk": pk, "version_pk": version_pk},
            )
            response = self.client.get(historic_version_url, format="json")
            self.assertEqual(response.data["id"], version_pk)
            self.assertEqual(response.data["field_dict"]["name"], name)

    def test_pagination_deleted(self):
        create_url = reverse("testmodelpaginated-list")

        for letter in string.ascii_lowercase:
            response = self.client.post(
                create_url, {"name": f"Foo_{letter}"}, format="json"
            )
            detail_url = reverse("testmodel-detail", kwargs={"pk": response.data["id"]})
            self.client.delete(detail_url, format="json")

        deleted_base_url = reverse("testmodelpaginated-deleted")
        for page, count in [(1, 10), (2, 10), (3, 6)]:
            query_kwargs = {"page": page}
            deleted_url = f"{deleted_base_url}?{urlencode(query_kwargs)}"
            response = self.client.get(deleted_url, format="json")
            self.assertEqual(response.data["count"], 26)
            self.assertEqual(len(response.data["results"]), count)


class TestModelsOriginalSerializerViewSetTests(AuthApiTestCase):
    def test_original_serializer(self):
        # create original parent with children: Bart & Lisa
        create_url = reverse("testparentmodel-list")
        data = {"children": [{"name": "Bart"}, {"name": "Lisa"}]}
        response = self.client.post(create_url, data, format="json")
        pk = response.data["id"]

        # update parent with children: Bart, Lisa & Maggie
        self.client.login(username="user2", password="password")
        update_url = reverse("testparentmodel-detail", kwargs={"pk": pk})
        data = {"children": [{"name": "Bart"}, {"name": "Lisa"}, {"name": "Maggie"}]}
        response = self.client.put(update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check that:
        history_url = reverse(
            "testparentmodel-history", kwargs={"pk": response.data["id"]}
        )
        response = self.client.get(history_url, format="json")
        # 1. there are two records in history
        self.assertEqual(len(response.data), 2)
        # 2. the ordering is correct
        self.assertGreater(
            response.data[0]["revision"]["date_created"],
            response.data[1]["revision"]["date_created"],
        )
        # 3. that the (historic) children are in the expected order,
        # e.g. most recent child-list first
        children_history = [
            [child["name"] for child in result["field_dict"]["children"]]
            for result in response.data
        ]
        self.assertListEqual(
            children_history, [["Bart", "Lisa", "Maggie"], ["Bart", "Lisa"]]
        )


class TestLimitedModelViewSetTests(AuthApiTestCase):
    def test_create_test_model(self):
        """
        Ensure we have history after creating a TestModel object.
        """
        url = reverse("testlimitedmodel-list")
        data = {"name": "Foo 1.1.0", "description": "Foo description"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse("testlimitedmodel-history", kwargs={"pk": response.data["id"]})
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 1)
        self.assertIsNotNone(response.data[0]["id"])
        self.assertIsNotNone(response.data[0]["revision"]["date_created"])
        self.assertEqual(response.data[0]["revision"]["user"], 1)
        self.assertIsNotNone(response.data[0]["revision"]["comment"])
        self.assertEqual(response.data[0]["field_dict"]["name"], "Foo 1.1.0")

    def test_editing_test_model(self):
        """
        Ensure we have history after editing a TestModel object.
        """
        url = reverse("testlimitedmodel-list")
        data = {"name": "Foo 1.2.0", "description": "Foo description"}
        response = self.client.post(url, data, format="json")

        self.client.login(username="user2", password="password")
        url = reverse("testlimitedmodel-detail", kwargs={"pk": response.data["id"]})
        data = {"name": "Foo 1.2.1"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse("testlimitedmodel-history", kwargs={"pk": response.data["id"]})
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 2)
        self.assertIsNotNone(response.data[0]["id"])
        self.assertIsNotNone(response.data[0]["revision"]["date_created"])
        self.assertEqual(response.data[0]["revision"]["user"], 2)
        self.assertIsNotNone(response.data[0]["revision"]["comment"])
        self.assertEqual(response.data[0]["field_dict"]["name"], "Foo 1.2.1")
        self.assertIsNotNone(response.data[1]["id"])
        self.assertIsNotNone(response.data[1]["revision"]["date_created"])
        self.assertEqual(response.data[1]["revision"]["user"], 1)
        self.assertIsNotNone(response.data[1]["revision"]["comment"])
        self.assertEqual(response.data[1]["field_dict"]["name"], "Foo 1.2.0")

    def test_deleting_test_model(self):
        """
        Ensure we have deletion history after deleting a TestModel object.
        """
        url = reverse("testlimitedmodel-list")
        data = {"name": "Foo 1.2.0", "description": "Foo description"}
        response = self.client.post(url, data, format="json")

        test_model_1 = TestLimitedModel.objects.get()
        url = reverse("testlimitedmodel-detail", kwargs={"pk": test_model_1.pk})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse("testlimitedmodel-deleted")
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 1)
        self.assertIsNotNone(response.data[0]["id"])
        self.assertIsNotNone(response.data[0]["revision"]["date_created"])
        self.assertEqual(response.data[0]["revision"]["user"], 1)
        self.assertIsNotNone(response.data[0]["revision"]["comment"])
        self.assertNotIn("id", response.data[0]["field_dict"])
        self.assertEqual(response.data[0]["field_dict"]["name"], "Foo 1.2.0")

    def test_reverting_test_model(self):
        """
        Ensure we have history after reverting a TestModel object.
        """
        url = reverse("testlimitedmodel-list")
        data = {"name": "Foo 1.2.0", "description": "Foo description"}
        response = self.client.post(url, data, format="json")

        self.client.login(username="user2", password="password")
        url = reverse("testlimitedmodel-detail", kwargs={"pk": response.data["id"]})
        data = {"name": "Foo 1.2.1"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        pk = response.data["id"]
        url = reverse("testlimitedmodel-history", kwargs={"pk": pk})
        response = self.client.get(url, format="json")

        url = reverse(
            "testlimitedmodel-revert",
            kwargs={
                "pk": pk,
                "version_pk": response.data[1]["id"],
            },
        )
        response = self.client.post(url, data, format="json")
        self.assertIsNotNone(response.data["id"])
        self.assertIsNotNone(response.data["revision"]["date_created"])
        self.assertEqual(response.data["revision"]["user"], 1)
        self.assertIsNotNone(response.data["revision"]["comment"])
        self.assertEqual(response.data["field_dict"]["name"], "Foo 1.2.0")

        url = reverse("testlimitedmodel-history", kwargs={"pk": pk})
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 3)
        self.assertIsNotNone(response.data[0]["id"])
        self.assertIsNotNone(response.data[0]["revision"]["date_created"])
        self.assertEqual(response.data[0]["revision"]["user"], 2)
        self.assertIsNotNone(response.data[0]["revision"]["comment"])
        self.assertEqual(response.data[0]["field_dict"]["name"], "Foo 1.2.0")
        self.assertIsNotNone(response.data[1]["id"])
        self.assertIsNotNone(response.data[1]["revision"]["date_created"])
        self.assertEqual(response.data[1]["revision"]["user"], 2)
        self.assertIsNotNone(response.data[1]["revision"]["comment"])
        self.assertEqual(response.data[1]["field_dict"]["name"], "Foo 1.2.1")
        self.assertIsNotNone(response.data[2]["id"])
        self.assertIsNotNone(response.data[2]["revision"]["date_created"])
        self.assertEqual(response.data[2]["revision"]["user"], 1)
        self.assertIsNotNone(response.data[2]["revision"]["comment"])
        self.assertEqual(response.data[2]["field_dict"]["name"], "Foo 1.2.0")


class TestRevertErrorCases(AuthApiTestCase):
    def test_revert_version_not_found(self):
        """
        Ensure reverting with a non-existent version_pk returns 404.
        """
        url = reverse("testmodel-list")
        response = self.client.post(url, {"name": "Original"}, format="json")
        pk = response.data["id"]

        url = reverse(
            "testmodel-revert",
            kwargs={"pk": pk, "version_pk": 99999},
        )
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Version Not Found")


class TestRestoreViewSetTests(AuthApiTestCase):
    def test_restore_deleted_object(self):
        """
        Ensure we can restore a deleted object.
        """
        url = reverse("testmodel-list")
        response = self.client.post(url, {"name": "Restorable"}, format="json")
        pk = response.data["id"]

        url = reverse("testmodel-detail", kwargs={"pk": pk})
        self.client.delete(url, format="json")
        self.assertEqual(TestModel.objects.filter(pk=pk).count(), 0)

        url = reverse("testmodel-deleted")
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 1)
        version_pk = response.data[0]["id"]

        url = reverse("testmodel-restore", kwargs={"version_pk": version_pk})
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Restorable")
        self.assertEqual(TestModel.objects.filter(pk=pk).count(), 1)

    def test_restore_version_not_found(self):
        """
        Ensure restoring with a non-existent version_pk returns 404.
        """
        url = reverse("testmodel-restore", kwargs={"version_pk": 99999})
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Version Not Found")

    def test_restore_clears_deleted_list(self):
        """
        Ensure a restored object no longer appears in the deleted list.
        """
        url = reverse("testmodel-list")
        response = self.client.post(url, {"name": "ToRestore"}, format="json")
        pk = response.data["id"]

        url = reverse("testmodel-detail", kwargs={"pk": pk})
        self.client.delete(url, format="json")

        url = reverse("testmodel-deleted")
        response = self.client.get(url, format="json")
        version_pk = response.data[0]["id"]

        url = reverse("testmodel-restore", kwargs={"version_pk": version_pk})
        self.client.post(url, format="json")

        url = reverse("testmodel-deleted")
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 0)


class TestFilterHistory(AuthApiTestCase):
    def test_filter_history_by_user(self):
        """
        Ensure history can be filtered by revision user.
        """
        url = reverse("testmodel-list")
        response = self.client.post(url, {"name": "v1"}, format="json")
        pk = response.data["id"]

        self.client.login(username="user2", password="password")
        url = reverse("testmodel-detail", kwargs={"pk": pk})
        self.client.patch(url, {"name": "v2"}, format="json")

        history_url = reverse("testmodel-history", kwargs={"pk": pk})

        response = self.client.get(history_url, format="json")
        self.assertEqual(len(response.data), 2)

        response = self.client.get(history_url, {"user": self.user1.pk}, format="json")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["field_dict"]["name"], "v1")

        response = self.client.get(history_url, {"user": self.user2.pk}, format="json")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["field_dict"]["name"], "v2")

    def test_filter_history_by_date(self):
        """
        Ensure history can be filtered by date_created.
        """
        url = reverse("testmodel-list")
        response = self.client.post(url, {"name": "v1"}, format="json")
        pk = response.data["id"]

        url = reverse("testmodel-detail", kwargs={"pk": pk})
        self.client.patch(url, {"name": "v2"}, format="json")

        history_url = reverse("testmodel-history", kwargs={"pk": pk})

        response = self.client.get(
            history_url, {"date_created__gt": "2099-01-01T00:00:00Z"}, format="json"
        )
        self.assertEqual(len(response.data), 0)

        response = self.client.get(
            history_url, {"date_created__lt": "2099-01-01T00:00:00Z"}, format="json"
        )
        self.assertEqual(len(response.data), 2)

    def test_filter_deleted_by_user(self):
        """
        Ensure deleted list can be filtered by revision user.
        """
        url = reverse("testmodel-list")
        response = self.client.post(url, {"name": "del1"}, format="json")
        pk1 = response.data["id"]

        self.client.login(username="user2", password="password")
        response = self.client.post(url, {"name": "del2"}, format="json")
        pk2 = response.data["id"]

        self.client.login(username="user1", password="password")
        self.client.delete(
            reverse("testmodel-detail", kwargs={"pk": pk1}), format="json"
        )
        self.client.login(username="user2", password="password")
        self.client.delete(
            reverse("testmodel-detail", kwargs={"pk": pk2}), format="json"
        )

        deleted_url = reverse("testmodel-deleted")

        response = self.client.get(deleted_url, format="json")
        self.assertEqual(len(response.data), 2)

        response = self.client.get(deleted_url, {"user": self.user1.pk}, format="json")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["field_dict"]["name"], "del1")


class TestUnauthenticatedAccess(APITestCase):
    def test_list_requires_auth(self):
        """
        Ensure unauthenticated users get 403.
        """
        url = reverse("testmodel-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_history_requires_auth(self):
        """
        Ensure unauthenticated users cannot access history.
        """
        url = reverse("testmodel-history", kwargs={"pk": 1})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deleted_requires_auth(self):
        """
        Ensure unauthenticated users cannot access deleted.
        """
        url = reverse("testmodel-deleted")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestCustomParamUrls(AuthApiTestCase):
    def setUp(self):
        super().setUp()
        self.record1 = TestModel.objects.create(name="test name")

    def test_url_with_extra_params(self):
        url = reverse("testmodel-history", kwargs={"pk": self.record1.pk})
        url = url.replace(
            "/test-app/test-models/",
            "/test-app/param/bar/test-models/",
        )
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
