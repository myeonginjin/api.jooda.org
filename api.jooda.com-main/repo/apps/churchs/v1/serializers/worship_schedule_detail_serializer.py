from rest_framework import serializers

from apps.churchs.models import ChurchWorshipSchedule

weekday = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

time_formatting = lambda time: time if len(str(time)) == 2 else "0" + str(time)


class ChurchWorshipScheduleDetailSerializer(serializers.ModelSerializer):
    church_worship_schedule_id = serializers.SerializerMethodField()
    church_id = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    weekday = serializers.SerializerMethodField()

    class Meta:
        model = ChurchWorshipSchedule
        fields = (
            "church_worship_schedule_id",
            "church_id",
            "title",
            "subtitle",
            "weekday",
            "place",
            "mc",
            "target",
            "reference",
            "time",
        )

    def get_church_worship_schedule_id(self, obj):
        return obj.id

    def get_church_id(self, obj):
        return obj.church.id

    def get_weekday(self, obj):
        try:
            return weekday[obj.weekday]
        except:
            return None

    def get_time(self, obj):
        try:
            time = f"{time_formatting(obj.start_time.hour)}:{time_formatting(obj.start_time.minute)}"
            if obj.end_time:
                time += f"~{time_formatting(obj.end_time.hour)}:{time_formatting(obj.end_time.minute)}"
            return time
        except:
            return None
