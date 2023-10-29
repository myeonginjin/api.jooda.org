from common import enums
from common.utils import secure
from .test_case import JoodaTestCase
from apps.accounts.models import Account


class AccountTestCase(JoodaTestCase):
    api_url = f"/{enums.ApiUrl.V1}accounts/"

    def setUp(self) -> None:
        self.account = Account.objects.create(
            name="test_account",
            birth_date="19980402",
            phone_number="010-0000-0000",
            password=secure.encrypte_data("1234"),
        )
        self.headers = {"HTTP_Authorization": self.account.id}
        return super().setUp()
