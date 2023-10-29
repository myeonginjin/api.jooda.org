from rest_framework import serializers
from apps.churchs.models import ChurchCalendar
from datetime import date


class ChurchCalendarListSerializer(serializers.ModelSerializer):
    calendar_id = serializers.SerializerMethodField()
    is_current_month = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()

    class Meta:
        model = ChurchCalendar
        fields = (
            "calendar_id",
            "title",
            "content",
            "start_date",
            "end_date",
            "is_current_month",
        )

    def get_calendar_id(self, obj):
        return obj.id

    def get_is_current_month(self, obj):
        today = date.today()
        obj_year = obj.start_date.year
        obj_month = obj.start_date.month

        if obj_year == today.year and obj_month == today.month:
            return True
        else:
            return False

    def get_end_date(self, obj):
        if obj.start_date == obj.end_date:
            return ""
        else:
            return obj.end_date
