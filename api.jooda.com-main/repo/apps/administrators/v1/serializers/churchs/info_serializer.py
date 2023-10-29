from rest_framework import serializers

from apps.churchs.models import Church


class ChurchInfoSerializer(serializers.ModelSerializer):
    church_id = serializers.SerializerMethodField()
    denomination = serializers.SerializerMethodField()
    denomination_list = serializers.SerializerMethodField()
    directions_parking = serializers.SerializerMethodField()
    directions_own_car = serializers.SerializerMethodField()
    directions_public_transport = serializers.SerializerMethodField()
    directions_shuttle_bus = serializers.SerializerMethodField()

    class Meta:
        model = Church
        fields = (
            "church_id",
            "name",
            "contact_number",
            "denomination",
            "denomination_list",
            "introduction_title",
            "introduction_content",
            "is_exposure",
            "address",
            "detail_address",
            "thumbnail",
            "logo",
            "directions_parking",
            "directions_own_car",
            "directions_public_transport",
            "directions_shuttle_bus",
        )

    def get_church_id(self, obj):
        try:
            return obj.id
        except:
            return ""

    def get_denomination(self, obj):
        try:
            return obj.denomination.name
        except:
            return ""

    def get_denomination_list(self, obj):
        return self.context.get("denomination_list", [])

    def get_directions_parking(self, obj):
        try:
            return obj.churchdirections.parking
        except:
            return ""

    def get_directions_own_car(self, obj):
        try:
            return obj.churchdirections.own_car
        except:
            return ""

    def get_directions_public_transport(self, obj):
        try:
            return obj.churchdirections.public_transport
        except:
            return ""

    def get_directions_shuttle_bus(self, obj):
        try:
            return obj.churchdirections.shuttle_bus
        except:
            return ""
