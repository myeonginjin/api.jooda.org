from rest_framework import serializers

from apps.churchs.models import ChurchWeekly


class ChurchWeeklyListSerializer(serializers.ModelSerializer):
    church_weekly_id = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = ChurchWeekly
        fields = (
            "church_weekly_id",
            "title",
            "image",
            "date",
        )

    def get_church_weekly_id(self, obj):
        return obj.id

    def get_date(self, obj):
        return f"20{obj.year}년 {obj.month}월"
