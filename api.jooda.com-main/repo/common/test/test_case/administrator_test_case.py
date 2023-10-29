from apps.administrators.models import Administrator
from common import enums
from common.utils import secure
from apps.administrators.v1 import utils

from .test_case import JoodaTestCase


class AdministratorTestCase(JoodaTestCase):
    api_url = f"/{enums.ApiUrl.V1}administrators/"

    def setUp(self) -> None:
        self.administrator = Administrator.objects.create(
            login_id="test_id",
            password=secure.encrypte_data("1234"),
            authorization_token=utils.create_authorization("test_id"),
        )
        self.headers = {"HTTP_Authorization": self.administrator.authorization_token}
        return super().setUp()
