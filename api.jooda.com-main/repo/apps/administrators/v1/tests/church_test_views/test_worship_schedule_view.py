from apps.churchs.models import (
    Church,
    ChurchDenomination,
    ChurchWorshipSchedule,
)
from common.test import test_case
from apps.administrators.v1 import serializers


class ChurchWorshipScheduleViewsTest(test_case.AdministratorTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.api_url += "churchs/worship_schedule/"
        denomination = ChurchDenomination.objects.create(name="테스트 종파")
        self.church = Church.objects.create(name="테스트 교회", denomination=denomination)
        self.administrator.church = self.church
        self.administrator.save(update_fields=["church"])

        church = Church.objects.create(name="테스트 교회", denomination=denomination)
        ChurchWorshipSchedule.objects.create(church=church)

        for i in range(3):
            ChurchWorshipSchedule.objects.create(
                church=self.church,
                title=f"title{i}",
                subtitle=f"subtitle{i}",
                weekday=f"{-1+i}",
                place=f"place{i}",
                mc=f"mc{i}",
                target=f"target{i}",
                reference=f"reference{i}",
                start_time=f"02:3{i}",
                end_time=f"03:3{i}",
            )

    def test_list(self):
        response = self.api_get()
        payload = self.get_content_from_response(response)
        self.assertValidatePayload(
            serializers.ChurchWorshipScheduleSerializer, response
        )

        self.assertEqual(payload[0]["weekday"], "일요일")
        self.assertEqual(len(payload), 3)

    def test_create(self):
        # wrong weekday, start and end time
        data = {
            "title": "title",
            "subtitle": "subtitle",
            "weekday": "weekday",
            "place": "place",
            "mc": "mc",
            "target": "target",
            "reference": "reference",
            "start_time": "start_time",
            "end_time": "end_time",
        }
        response = self.api_post(data)
        self.assertEqual(self.get_content_from_response(response), 406)

        # wrong weekday
        data = {
            "title": "title",
            "subtitle": "subtitle",
            "weekday": "dad",
            "place": "place",
            "mc": "mc",
            "target": "target",
            "reference": "reference",
            "start_time": "14:12",
        }
        response = self.api_post(data)
        self.assertEqual(self.get_content_from_response(response), 406)

        # wrong start and end time
        data = {
            "title": "title",
            "subtitle": "subtitle",
            "weekday": "5",
            "place": "place",
            "mc": "mc",
            "target": "target",
            "reference": "reference",
            "start_time": "14:12",
            "end_time": "12:12",
        }
        response = self.api_post(data)
        self.assertEqual(self.get_content_from_response(response), 406)

        # success
        data = {
            "title": "title",
            "subtitle": "subtitle",
            "weekday": "-1",
            "place": "place",
            "mc": "mc",
            "target": "target",
            "reference": "reference",
            "start_time": "14:12",
            "end_time": "15:12",
        }
        response = self.api_post(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ChurchWorshipSchedule.objects.all().count(), 5)

    def test_patch(self):
        church_worship_schedule = ChurchWorshipSchedule.objects.get(weekday=-1)
        # 시작 시간보다 마감 시간이 빠를 때
        data = {
            "church_worship_schedule_id": church_worship_schedule.id,
            "end_time": "01:00",
        }
        response = self.api_patch(data)

        # 성공, 마감 시간을 잘 주었을 때
        data = {
            "church_worship_schedule_id": church_worship_schedule.id,
            "end_time": "11:00",
        }
        response = self.api_patch(data)
        church_worship_schedule = ChurchWorshipSchedule.objects.get(weekday=-1)
        self.assertEqual(str(church_worship_schedule.start_time), "02:30:00")
        self.assertEqual(str(church_worship_schedule.end_time), "11:00:00")
        self.assertEqual(response.status_code, 200)

        # 잘못된 요일 정보
        data = {
            "church_worship_schedule_id": church_worship_schedule.id,
            "weekday": "asd",
        }
        response = self.api_patch(data)
        self.assertEqual(self.get_content_from_response(response), 406)

        # 성공
        data = {
            "church_worship_schedule_id": church_worship_schedule.id,
            "weekday": "0",
            "start_time": "1:00",
        }
        response = self.api_patch(data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ChurchWorshipSchedule.objects.filter(weekday=-1).exists(), 0)
        church_worship_schedule = ChurchWorshipSchedule.objects.get(
            id=church_worship_schedule.id
        )
        attrs = ["title", "subtitle", "place", "mc", "target", "reference"]
        for attr in attrs:
            self.assertEqual(getattr(church_worship_schedule, attr), f"{attr}{0}")
        self.assertEqual(church_worship_schedule.weekday, 0)
        self.assertEqual(str(church_worship_schedule.start_time), "01:00:00")
        self.assertEqual(str(church_worship_schedule.end_time), "11:00:00")

    def test_delete(self):
        church_worship_schedule = ChurchWorshipSchedule.objects.get(weekday=-1)
        data = {
            "church_worship_schedule_id": church_worship_schedule.id,
        }
        self.api_url += "delete/"

        response = self.api_post(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ChurchWorshipSchedule.objects.all().count(), 3)
