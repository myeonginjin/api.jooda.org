from rest_framework import serializers
from apps.churchs.models import ChurchWorshipSchedule
from collections import defaultdict

weekday = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

time_formatting = lambda time: time if len(str(time)) == 2 else "0" + str(time)


class ChurchWorshipScheduleListSerializer:
    def __new__(self, church_worship_schedule_list):
        payload = {}
        payload["church_worship_schedule_list"] = self.get_church_worship_schedule_list(
            church_worship_schedule_list
        )
        return payload

    def get_church_worship_schedule_list(
        church_worship_schedule_list: ChurchWorshipSchedule,
    ) -> list:
        title_grouped_objects = defaultdict(list)

        for obj in church_worship_schedule_list:
            title_grouped_objects[obj.title].append(obj)

        result = []

        for title, objs in title_grouped_objects.items():
            worship_schedule_list = []
            for obj in objs:
                time = f"{time_formatting(obj.start_time.hour)}:{time_formatting(obj.start_time.minute)}"
                if obj.end_time:
                    time += f"~{time_formatting(obj.end_time.hour)}:{time_formatting(obj.end_time.minute)}"
                worship_schedule_list.append(
                    {
                        "church_worship_schedule_id": getattr(obj, "id", None),
                        "subtitle": getattr(obj, "subtitle", None),
                        "weekday": weekday[obj.weekday],
                        "place": getattr(obj, "place", None),
                        "mc": getattr(obj, "mc", None),
                        "target": getattr(obj, "target", None),
                        "reference": getattr(obj, "reference", None),
                        "time": time,
                    }
                )

            result.append(
                {
                    "title": title,
                    "worship_schedule_list": worship_schedule_list,
                }
            )

        return result
