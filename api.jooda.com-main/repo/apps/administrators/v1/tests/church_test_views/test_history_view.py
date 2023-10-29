from apps.churchs.models import (
    Church,
    ChurchDenomination,
    ChurchHistory,
)
from common.test import test_case
from apps.administrators.v1 import serializers


class ChurchHistoryViewsTest(test_case.AdministratorTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.api_url += "churchs/history/"
        denomination = ChurchDenomination.objects.create(name="테스트 종파")
        self.church = Church.objects.create(name="테스트 교회", denomination=denomination)
        self.administrator.church = self.church
        self.administrator.save(update_fields=["church"])
        self.church_history = ChurchHistory.objects.create(
            church=self.church, year="21", month="07", day="11", content="1234444"
        )
        self.church_history1 = ChurchHistory.objects.create(
            church=self.church, year="22", month="04", day="22", content="1234444"
        )
        self.church_history2 = ChurchHistory.objects.create(
            church=self.church, year="23", month="05", day="22", content="1234444"
        )

    def test_list(self):
        response = self.api_get()
        self.assertValidatePayload(serializers.ChurchHistorySerializer, response)

    def test_create(self):
        wrong_data = {
            "history_list": [
                {"year": "23", "month": "04", "day": "33", "content": "내용"},
                {"year": "22", "month": "04", "day": "30", "content": "내용"},
            ],
        }
        data = {
            "history_list": [
                {"year": "23", "month": "04", "day": "3", "content": "내용"},
                {"year": "22", "month": "04", "day": "30", "content": "내용"},
            ],
        }

        response = self.api_post(data=wrong_data)

        self.api_post(data=data)

        self.assertEqual(self.get_content_from_response(response), 406)

        histories = ChurchHistory.objects.filter(content="내용").order_by(
            "-year", "-month", "-day"
        )

        self.assertEqual(histories[0].day, "03")
        self.assertEqual(histories[1].year, "22")

    def test_patch(self):
        data = {
            "history_list": [
                {
                    "church_history_id": f"{self.church_history.id}",
                    "year": 2021,
                    "month": 4,
                    "content": "@52414525",
                },
            ]
        }
        response = self.api_patch(data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ChurchHistory.objects.get(year="21").content, "@52414525")

        wrong_data = {
            "history_list": [
                {
                    "church_history_id": f"{self.church_history.id}",
                    "month": 74,
                },
            ]
        }
        response = self.api_patch(data=wrong_data)
        self.assertEqual(self.get_content_from_response(response), 406)

        data = {
            "history_list": [
                {
                    "church_history_id": f"{self.church_history.id}",
                    "content": "@52414525dsnajkndksjandkjsankjdsanjdk",
                },
            ]
        }
        self.api_patch(data=data)
        self.assertEqual(
            ChurchHistory.objects.get(id=self.church_history.id).content,
            "@52414525dsnajkndksjandkjsankjdsanjdk",
        )

    def test_delete(self):
        self.api_url += "delete/"
        data = {
            "history_list": [
                f"{self.church_history.id}",
                f"{self.church_history1.id}",
            ]
        }

        response = self.api_post(data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(ChurchHistory.objects.all()), 1)
