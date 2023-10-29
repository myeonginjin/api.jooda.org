from rest_framework import serializers

from apps.administrators.models import Administrator


class AccountInfoSerializer(serializers.ModelSerializer):
    administrator_id = serializers.SerializerMethodField()
    church_id = serializers.SerializerMethodField()
    authorization_token = serializers.SerializerMethodField()

    class Meta:
        model = Administrator
        fields = (
            "administrator_id",
            "church_id",
            "authorization_token",
        )

    def get_administrator_id(self, obj):
        return obj.id

    def get_church_id(self, obj):
        if obj.church:
            return obj.church.id
        else:
            return ""

    def get_authorization_token(self, obj):
        return self.context.get("authorization_token", obj.authorization_token)
