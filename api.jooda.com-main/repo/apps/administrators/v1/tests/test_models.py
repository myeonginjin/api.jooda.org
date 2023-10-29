from django.test import TestCase
from apps.administrators.models import Administrator
from apps.churchs.models import Church
from common.utils import secure


class AdministratorModelsTest(TestCase):
    def setUp(self) -> None:
        self.church = Church.objects.create(name="테스트 교회", address="테스트 주소")
        self.administrator = Administrator.objects.create(
            login_id="test", password="1234", church=self.church
        )
        return super().setUp()

    def test_hash_password(self):
        self.assertEquals(
            secure.encrypte_data(self.administrator.password),
            "5de5ab37c6abcaa2fa9d9c192976561dfd3bd950c26d10b6be90e47efe7f2339",
            msg="비밀번호 해시 오류 / Salt 값 이상",
        )
        self.assertEquals(
            len(secure.encrypte_data(self.administrator.password)),
            64,
            msg="비밀번호 해시 길이 오류",
        )
