from apps.churchs.models import (
    Church,
    ChurchDenomination,
    ChurchCalendar,
)
from common.test import test_case
from apps.administrators.v1 import serializers


class ChurchCalendarViewsTest(test_case.AdministratorTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.api_url += "churchs/calendar/"
        denomination = ChurchDenomination.objects.create(name="테스트 종파")
        self.church = Church.objects.create(name="테스트 교회", denomination=denomination)
        church = Church.objects.create(name="테스트 교회", denomination=denomination)
        ChurchCalendar.objects.create(church=church)
        self.administrator.church = self.church
        self.administrator.save(update_fields=["church"])
        for i in range(1, 4):
            ChurchCalendar.objects.create(
                church=self.church,
                title=f"title{i}",
                content=f"content{i}",
                start_date=f"2023-01-0{i}",
                end_date=f"2023-01-{i}1",
            )

    def test_list(self):
        data = {
            "year": 2023,
            "month": 1,
        }
        response = self.api_get(data)
        self.assertValidatePayload(serializers.ChurchCalendarSerializer, response)

        response = self.api_get()
        payload = self.get_content_from_response(response)

        self.assertEqual(len(payload), 0)

    def test_create(self):
        # 잘못된 시작, 마감 날짜
        data = {
            "title": "title",
            "content": "content",
            "start_date": "start_date",
            "end_date": "end_date",
        }
        response = self.api_post(data)
        self.assertEqual(self.get_content_from_response(response), 406)

        # 필수 파라미터 전송 X
        data = {
            "title": "title",
            "content": "content",
        }
        response = self.api_post(data)
        self.assertEqual(self.get_content_from_response(response), 400)

        # 성공
        data = {
            "title": "title",
            "content": "content",
            "start_date": "2023-03-04",
            "end_date": "2023-03-05",
        }
        response = self.api_post(data)
        self.assertEqual(response.status_code, 200)

        # 성공
        data = {
            "title": "title22",
            "content": "content",
            "start_date": "2023-03-04",
            "end_date": "2023-03-04",
        }
        response = self.api_post(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ChurchCalendar.objects.get(title="title22").end_date, None)
        self.assertEqual(ChurchCalendar.objects.all().count(), 6)

    def test_patch(self):
        church_calendar = ChurchCalendar.objects.get(title="title1")

        # 잘못된 시작, 마감 날짜
        data = {
            "church_calendar_id": church_calendar.id,
            "start_date": "start_date",
            "end_date": "end_date",
        }
        response = self.api_patch(data)
        self.assertEqual(self.get_content_from_response(response), 406)

        data = {
            "church_calendar_id": church_calendar.id,
            "end_date": "2022-01-23",
        }
        response = self.api_patch(data)
        self.assertEqual(self.get_content_from_response(response), 406)

        data = {
            "church_calendar_id": church_calendar.id,
            "end_date": "24-1-10",
        }
        response = self.api_patch(data)
        self.assertEqual(response.status_code, 200)

        data = {
            "church_calendar_id": church_calendar.id,
            "content": "contenttttt",
            "start_date": "2024-01-02",
        }
        response = self.api_patch(data)
        self.assertEqual(response.status_code, 200)
        church_calendar = ChurchCalendar.objects.get(id=church_calendar.id)
        self.assertEqual(church_calendar.content, "contenttttt")
        self.assertEqual(church_calendar.title, "title1")
        self.assertEqual(str(church_calendar.start_date), "2024-01-02")
        self.assertEqual(str(church_calendar.end_date), "2024-01-10")

    def test_delete(self):
        self.api_url += "delete/"

        church_calendar = ChurchCalendar.objects.get(title="title1")
        data = {
            "church_calendar_id": church_calendar.id,
        }

        response = self.api_post(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ChurchCalendar.objects.all().count(), 3)

        church_calendar = ChurchCalendar.objects.get(title=None)
        data = {
            "church_calendar_id": church_calendar.id,
        }
        response = self.api_post(data)
        self.assertEqual(self.get_content_from_response(response), 403)
