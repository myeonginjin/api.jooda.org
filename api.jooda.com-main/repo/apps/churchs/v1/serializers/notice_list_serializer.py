from rest_framework import serializers

from apps.churchs.models import ChurchNotice


class ChurchNoticeListSerializer(serializers.ModelSerializer):
    church_notice_id = serializers.SerializerMethodField()

    class Meta:
        model = ChurchNotice
        fields = (
            "church_notice_id",
            "title",
            "created_at",
        )

    def get_church_notice_id(self, obj):
        return obj.id
