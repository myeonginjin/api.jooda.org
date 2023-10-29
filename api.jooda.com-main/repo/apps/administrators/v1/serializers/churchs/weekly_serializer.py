from rest_framework import serializers

from apps.churchs.models import ChurchWeekly


class ChurchWeeklySerializer(serializers.ModelSerializer):
    church_weekly_id = serializers.SerializerMethodField()

    class Meta:
        model = ChurchWeekly
        fields = (
            "church_weekly_id",
            "title",
            "image",
            "created_at",
            "year",
            "month",
        )

    def get_church_weekly_id(self, obj):
        return obj.id
