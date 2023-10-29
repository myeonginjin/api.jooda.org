from apps.churchs.models import (
    Church,
    ChurchDenomination,
    ChurchWeekly,
)
from common.test import test_case
from apps.administrators.v1 import serializers


class ChurchWeeklyViewsTest(test_case.AdministratorTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.api_url += "churchs/weekly/"
        denomination = ChurchDenomination.objects.create(name="테스트 종파")
        self.church = Church.objects.create(name="테스트 교회", denomination=denomination)
        self.administrator.church = self.church
        self.administrator.save(update_fields=["church"])

        church1 = Church.objects.create(name="테스", denomination=denomination)
        self.other_church_weekly = ChurchWeekly.objects.create(
            church=church1,
            title="test1",
        )
        self.church_weekly = ChurchWeekly.objects.create(
            church=self.church,
            title="test1",
        )
        self.church_weekly1 = ChurchWeekly.objects.create(
            church=self.church,
            title="test2",
        )
        self.church_weekly2 = ChurchWeekly.objects.create(
            church=self.church,
            title="test3",
        )

    def test_list(self):
        response = self.api_get()
        self.assertValidatePayload(serializers.ChurchWeeklySerializer, response)

    def test_create(self):
        data = {
            "title": "테스트",
            "image": self.image,
        }
        wrong_data = {
            "title": "테스트",
        }

        response = self.api_post(data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ChurchWeekly.objects.all().count(), 5)
        response = self.api_post(wrong_data)
        self.assertEqual(self.get_content_from_response(response), 400)

    def test_patch(self):
        data = {
            "church_weekly_id": f"{self.church_weekly.id}",
            "title": "테스트",
            "image": self.image,
        }
        wrong_data = {
            "church_weekly_id": f"{self.other_church_weekly.id}",
            "title": "테스트",
        }

        response = self.api_patch(wrong_data)
        self.assertEqual(self.get_content_from_response(response), 403)

        response = self.api_patch(data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            len(ChurchWeekly.objects.get(id=self.church_weekly.id).image.url) > 1
        )

        data = {
            "church_weekly_id": f"{self.church_weekly.id}",
            "title": "테스트",
            "image": self.image,
            "is_delete_image": True,
        }
        response = self.api_patch(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ChurchWeekly.objects.get(id=self.church_weekly.id).image, "")

    def test_delete(self):
        self.api_url += "delete/"
        data = {
            "church_weekly_id": f"{self.church_weekly.id}",
        }
        wrong_data = {
            "church_weekly_id": f"{self.other_church_weekly.id}",
        }
        response = self.api_post(wrong_data)
        self.assertEqual(self.get_content_from_response(response), 403)

        response = self.api_post(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ChurchWeekly.objects.all().count(), 3)
