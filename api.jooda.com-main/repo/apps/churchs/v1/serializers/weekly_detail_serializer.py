from rest_framework import serializers
from apps.churchs.models import ChurchWeekly


class ChurchWeeklyDetailSerializer(serializers.ModelSerializer):
    church_weekly_id = serializers.SerializerMethodField()
    church_id = serializers.SerializerMethodField()

    class Meta:
        model = ChurchWeekly
        fields = (
            "church_weekly_id",
            "church_id",
            "image",
        )

    def get_church_weekly_id(self, obj):
        return obj.id

    def get_church_id(self, obj):
        return obj.church.id
