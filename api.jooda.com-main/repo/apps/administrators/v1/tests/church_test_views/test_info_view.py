from apps.administrators.models import Administrator
from apps.churchs.models import (
    Church,
    ChurchDenomination,
)
from common.test import test_case
from common.utils import secure
from apps.administrators.v1 import utils
from apps.administrators.v1 import serializers


class ChurchInfoViewsTest(test_case.AdministratorTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.api_url += "churchs/info/"
        self.administrator2 = Administrator.objects.create(
            login_id="test2",
            password=secure.encrypte_data("1234"),
            authorization_token=utils.create_authorization("test2"),
        )

    def test_list(self):
        response = self.api_get()
        self.assertEqual(
            self.get_content_from_response(response),
            403,
            msg="등록된 교회가 없는 관리자 에러 확인",
        )
        ChurchDenomination.objects.bulk_create(
            ChurchDenomination(name=i) for i in range(10)
        )
        self.administrator.church = Church.objects.create(
            name="test_info",
            denomination=ChurchDenomination.objects.get(name=4),
        )
        self.administrator.save(update_fields=["church"])
        response = self.api_get()
        self.assertValidatePayload(serializers.ChurchInfoSerializer, response)

    def test_create(self):
        data = {
            "church_name": "테스트 교회",
            "contact_number": "010-3434-2525",
            "denomination_name": "대한 장로회",
            "introduction_title": "오늘도 아멘",
            "introduction_content": "내일도 아멘",
            "address": "경기도 안산시 상록구 석호공원로 8",
        }
        self.assertEqual(ChurchDenomination.objects.count(), 0)
        self.assertEqual(
            self.administrator.church, None, msg="교회 등록안한 관리자에 교회 등록이 되어있음"
        )

        response = self.api_post(data=data)
        self.assertValidatePayload(serializers.AccountInfoSerializer, response)

        data = {
            "church_name": "테스트 교회2",
            "contact_number": "010-3434-2525",
            "denomination_name": "대한 장로회",
            "introduction_title": "오늘도 아멘2",
            "introduction_content": "내일도 아멘2",
            "address": "경기도 안산시 상록구 석호공원로 8",
        }

        response = self.api_post(data=data)

        headers = {"HTTP_Authorization": self.administrator2.authorization_token}
        response = self.api_post(data=data, headers=headers)
        administrators = Administrator.objects.all()
        self.assertEqual(
            administrators[0].church.denomination,
            administrators[1].church.denomination,
        )

    def test_patch(self):
        church = Church.objects.create(name="테스트 교회")
        self.administrator.church = church
        self.administrator.save(update_fields=["church"])
        data = {
            "church_name": "테스트 교회",
            "contact_number": "010-3434-2525",
            "denomination_name": "대한 장로회",
            "introduction_title": "오늘도 아멘",
            "address": "경기도 안산시 상록구 석호공원로 8",
            "thumbnail": self.image,
        }
        self.assertEqual(ChurchDenomination.objects.all().count(), 0)
        response = self.api_patch(data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ChurchDenomination.objects.all().count(), 1)

        church = Church.objects.get(id=church.id)
        self.assertEqual(church.name, "테스트 교회")
        self.assertEqual(church.contact_number, "010-3434-2525")
        self.assertEqual(church.denomination.name, "대한 장로회")
        self.assertIsNone(church.introduction_content)
        self.assertTrue(len(church.longitude) != 0)
        self.assertTrue(len(church.latitude) != 0)
        self.assertTrue(len(church.thumbnail.url) != 0)
        longitude, latitude = church.longitude, church.latitude

        data = {
            "address": "경기도 안산시 상록구 학사 4길 18-1",
            "is_delete_thumbnail": True,
        }
        response = self.api_patch(data=data)
        church = Church.objects.get(id=church.id)
        self.assertNotEqual(church.longitude, longitude)
        self.assertNotEqual(church.latitude, latitude)
        self.assertEqual(church.thumbnail, "")
