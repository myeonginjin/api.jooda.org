from rest_framework import serializers
from .pastors_serializer import ChurchPastorsSerializer
from .history_serializer import ChurchHistorySerializer
from .directions_serializer import ChurchDirectionsSerializer
from apps.churchs.models import Church


class ChurchIntroductionSerializer(serializers.ModelSerializer):
    church_id = serializers.SerializerMethodField()
    directions = serializers.SerializerMethodField()
    pastor_list = serializers.SerializerMethodField()
    history_list = serializers.SerializerMethodField()

    class Meta:
        model = Church
        fields = (
            ("church_id"),
            ("name"),
            ("contact_number"),
            ("longitude"),
            ("latitude"),
            ("address"),
            ("detail_address"),
            ("directions"),
            ("pastor_list"),
            ("thumbnail"),
            ("history_list"),
        )

    def get_church_id(self, obj):
        return obj.id

    def get_directions(self, obj):
        church_directions = getattr(obj, "churchdirections", None)
        return ChurchDirectionsSerializer(church_directions).data

    def get_pastor_list(self, obj):
        return ChurchPastorsSerializer(
            obj.church_pastor.all().order_by("order")[:6], many=True
        ).data

    def get_history_list(self, obj):
        return ChurchHistorySerializer(
            obj.church_history.all().order_by("-year", "-month", "-day")[:5],
            many=True,
        ).data
