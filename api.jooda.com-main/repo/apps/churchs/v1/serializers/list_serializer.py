from rest_framework import serializers
from apps.churchs.models import Church


class ChurchListSerializer(serializers.ModelSerializer):
    church_id = serializers.SerializerMethodField()

    class Meta:
        model = Church
        fields = (
            ("church_id"),
            ("name"),
            ("address"),
            ("logo"),
        )

    def get_church_id(self, obj):
        return obj.id
