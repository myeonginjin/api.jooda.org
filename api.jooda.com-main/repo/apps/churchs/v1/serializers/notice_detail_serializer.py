from rest_framework import serializers
from apps.churchs.models import ChurchNotice


class ChurchNoticeDetailSerializer(serializers.ModelSerializer):
    church_notice_id = serializers.SerializerMethodField()
    church_id = serializers.SerializerMethodField()

    class Meta:
        model = ChurchNotice
        fields = (
            "church_notice_id",
            "church_id",
            "title",
            "content",
            "created_at",
            "image",
        )

    def get_church_notice_id(self, obj):
        return obj.id

    def get_church_id(self, obj):
        return obj.church.id
