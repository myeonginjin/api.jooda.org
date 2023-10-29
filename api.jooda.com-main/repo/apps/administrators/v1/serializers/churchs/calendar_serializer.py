from common import format
from rest_framework import serializers
from apps.churchs.models import ChurchCalendar
from datetime import date


class ChurchCalendarSerializer(serializers.ModelSerializer):
    church_calendar_id = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    is_current_month = serializers.SerializerMethodField()

    class Meta:
        model = ChurchCalendar
        fields = (
            "church_calendar_id",
            "title",
            "content",
            "start_date",
            "end_date",
            "is_current_month",
        )

    def get_church_calendar_id(self, obj):
        return obj.id

    def get_end_date(self, obj):
        if obj.start_date == obj.end_date:
            return ""
        else:
            return obj.end_date

    def get_is_current_month(self, obj):
        end_date = getattr(obj, "end_date", None)
        if format.month(obj.start_date.month) == self.context.get(
            "month", "00"
        ) or format.month(end_date.month if end_date else "-1") == self.context.get(
            "month", "00"
        ):
            return True
        else:
            return False
