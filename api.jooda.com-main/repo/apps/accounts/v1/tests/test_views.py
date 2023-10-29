from apps.accounts.models import Account
from common.test import test_case
from common import enums


class ViewsTest(test_case.AccountTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_message_authentication(self):
        self.api_url += "message_authentication/"
        data = {"phone_number": "010-8849-6376"}
        response = self.api_post(data)
        self.assertFalse(
            self.get_content_from_response(response)["is_duplicated_phone_number"]
        )
        Account.objects.create(phone_number="010-8849-6376")
        response = self.api_post(data)
        self.assertTrue(
            self.get_content_from_response(response)["is_duplicated_phone_number"]
        )

    def test_create(self):
        data = {
            "name": "name",
            "phone_number": "010-8849-6376",
            "password": "password",
            "gender": "M",
            "birth_date": "birth_date",
        }
        self.headers["HTTP_os"] = "os"
        self.headers["HTTP_device_id"] = "device_id"
        self.headers["HTTP_fcm_token"] = "fcm_token"
        response = self.api_post(data)
        self.assertEqual(
            self.get_content_from_response(response), 400, msg="헤더에 정보 덜 넣은 경우"
        )
        self.headers["HTTP_app_version"] = "1.0.0"
        response = self.api_post(data)
        self.assertEqual(response.status_code, 200, msg="정상 헤더 내용")
        response = self.api_post(data)
        self.assertEqual(
            self.get_content_from_response(response), 402, "이미 있는 전화번호로 등록 신청"
        )
        data["name"] = "name2"
        data["inquire"] = True
        response = self.api_post(data)
        self.assertEqual(
            Account.objects.filter(name="name2").get().state,
            enums.AccountState.WAIT_FOR,
        )
        self.assertEqual(
            Account.objects.filter(name="name").get().state,
            enums.AccountState.IN_ACTIVE,
        )

    def test_login(self):
        self.api_url += "login/"
        data = {"phone_number": "010-0000-0000"}
        response = self.api_post(data)
        self.assertEqual(self.get_content_from_response(response), 400)
        data["password"] = "1234"
        response = self.api_post(data)
        self.assertEqual(self.get_content_from_response(response), str(self.account.id))
        data["password"] = 1234
        response = self.api_post(data)
        self.assertEqual(self.get_content_from_response(response), str(self.account.id))
        data["phone_number"] = "010-0000-1234"
        response = self.api_post(data)
        self.assertEqual(self.get_content_from_response(response), 403)

    def test_check(self):
        self.api_url += "check/"
        data = {"phone_number": "010-0000-0000"}
        response = self.api_post(data)
        self.assertEqual(self.get_content_from_response(response), 400)
        data = {
            "name": "test_account",
            "birth_date": "19980402",
            "phone_number": "010-0000-0000",
        }
        self.api_post(data)
        response = self.api_post(data)
        self.assertEqual(self.get_content_from_response(response), str(self.account.id))
        data["phone_number"] = "010-0000-1234"
        response = self.api_post(data)
        self.assertEqual(self.get_content_from_response(response), 403)

    def test_patch(self):
        self.account.state = enums.AccountState.IN_ACTIVE
        self.account.save()
        data = {
            "name": "name",
            "gender": "F",
            "birth_date": "20001230",
        }
        self.api_patch(data)
        account = Account.objects.get(id=self.account.id)
        self.assertEqual(account.state, enums.AccountState.IN_ACTIVE)
        data = {"phone_number": "010-1234-5678"}
        self.api_patch(data)
        account = Account.objects.get(id=self.account.id)
        self.assertEqual(account.state, enums.AccountState.ACTIVE)
