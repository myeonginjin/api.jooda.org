from apps.administrators.models import Administrator
from apps.churchs.models import Church
from common.utils import secure
from apps.administrators.v1 import serializers
from common.test import test_case


class AdministratorAccountViewsTest(test_case.AdministratorTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.api_url += "accounts/"
        self.church = Church.objects.create(name="테스트 교회", address="테스트 주소")
        self.administrator = Administrator.objects.create(
            login_id="test", password=secure.encrypte_data("1234"), church=self.church
        )
        self.administrators = Administrator.objects.all()

    def test_create(self):
        # hash password
        data = {"id": "test2", "password": "1234", "phone_number": "01088496376"}
        response = self.api_post(data)
        new_administrator = self.administrators.get(login_id="test2")
        self.assertEqual(
            new_administrator.password,
            "5de5ab37c6abcaa2fa9d9c192976561dfd3bd950c26d10b6be90e47efe7f2339",
            msg="관리자 계정 비밀번호 암호화 에러",
        )

        # duplicated id
        data = {"id": "test2", "password": "1234", "phone_number": "01088496376"}
        response = self.api_post(data)
        response_data = self.get_content_from_response(response)
        self.assertEqual(response_data, 402, msg="같은 ID 회원가입")

        # BAD REQUEST
        data = {"password": "1234", "phone_number": "01088496376"}
        response = self.api_post(data)
        response_data = self.get_content_from_response(response)
        self.assertEqual(response_data, 400, msg="필수 파라미터 안줬을 때")

    def test_login(self):
        self.api_url += "login/"

        data = {"id": "test", "password": "1234"}
        response = self.api_post(data)

        self.assertValidatePayload(serializers.AccountInfoSerializer, response)

        administrator = Administrator.objects.get(login_id="test")
        self.assertEqual(
            self.get_content_from_response(response)["authorization_token"],
            administrator.authorization_token,
        )
