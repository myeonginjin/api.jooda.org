from apps.churchs.models import (
    Church,
    ChurchDenomination,
    ChurchNotice,
)
from common.test import test_case

from apps.administrators.v1 import serializers


class ChurchNoticeViewsTest(test_case.AdministratorTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.api_url += "churchs/notice/"
        denomination = ChurchDenomination.objects.create(name="테스트 종파")
        self.church = Church.objects.create(name="테스트 교회", denomination=denomination)
        self.administrator.church = self.church
        self.administrator.save(update_fields=["church"])

        church1 = Church.objects.create(name="테스", denomination=denomination)

        self.other_church_notice = ChurchNotice.objects.create(
            church=church1,
            title="test1",
            content="content1",
        )
        self.church_notice = ChurchNotice.objects.create(
            church=self.church,
            writer=self.administrator,
            title="test1",
            content="content1",
        )
        self.church_notice1 = ChurchNotice.objects.create(
            church=self.church,
            writer=self.administrator,
            title="test2",
            content="content2",
        )
        self.church_notice2 = ChurchNotice.objects.create(
            church=self.church,
            writer=self.administrator,
            title="test3",
            content="content3",
        )

    def test_list(self):
        response = self.api_get()
        self.assertValidatePayload(serializers.ChurchNoticeSerializer, response)

    def test_create(self):
        data = {
            "title": "테스트",
            "content": "contetntttt",
            "image": self.image,
        }
        wrong_data = {
            "title": "테스트",
        }

        response = self.api_post(data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ChurchNotice.objects.all().count(), 5)
        response = self.api_post(wrong_data)
        self.assertEqual(self.get_content_from_response(response), 400)

    def test_patch(self):
        data = {
            "church_notice_id": f"{self.church_notice.id}",
            "title": "테스트",
            "content": "contetntttt",
            "image": self.image,
        }
        wrong_data = {
            "church_notice_id": f"{self.other_church_notice.id}",
            "title": "테스트",
        }

        response = self.api_patch(wrong_data)
        self.assertEqual(self.get_content_from_response(response), 403)

        response = self.api_patch(data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            len(ChurchNotice.objects.get(id=self.church_notice.id).image.url) > 1
        )

        data = {
            "church_notice_id": f"{self.church_notice.id}",
            "title": "테스트",
            "content": "contetntttt",
            "image": self.image,
            "is_delete_image": True,
        }
        response = self.api_patch(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ChurchNotice.objects.get(id=self.church_notice.id).image, "")

    def test_delete(self):
        self.api_url += "delete/"
        data = {
            "church_notice_id": f"{self.church_notice.id}",
        }
        wrong_data = {
            "church_notice_id": f"{self.other_church_notice.id}",
        }
        response = self.api_post(wrong_data)
        self.assertEqual(self.get_content_from_response(response), 403)

        response = self.api_post(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ChurchNotice.objects.all().count(), 3)
