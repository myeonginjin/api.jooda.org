from rest_framework import serializers

from apps.churchs.models import ChurchPastor


class ChurchPastorSerializer(serializers.ModelSerializer):
    church_pastor_id = serializers.SerializerMethodField()

    class Meta:
        model = ChurchPastor
        fields = (
            "church_pastor_id",
            "name",
            "role",
            "image",
        )

    def get_church_pastor_id(self, obj):
        return obj.id
