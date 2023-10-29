from rest_framework import serializers

from apps.churchs.models import ChurchHistory


class ChurchHistorySerializer(serializers.ModelSerializer):
    church_history_id = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = ChurchHistory
        fields = ("church_history_id", "date", "content")

    def get_church_history_id(self, obj):
        return obj.id

    def get_date(self, obj):
        return obj.year + "." + obj.month + "." + obj.day
