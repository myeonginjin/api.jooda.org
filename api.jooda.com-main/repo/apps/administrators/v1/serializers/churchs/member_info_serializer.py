from rest_framework import serializers

from apps.accounts.models import Account


class ChurchMemberInfoSerializer(serializers.ModelSerializer):
    account_id = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    birth_date = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = (
            "account_id",
            "name",
            "gender",
            "phone_number",
            "birth_date",
        )

    def get_account_id(self, obj):
        return obj.id

    def get_gender(self, obj):
        if obj.gender == "M":
            return "남성"
        else:
            return "여성"

    def get_birth_date(self, obj):
        try:
            return (
                obj.birth_date[2:4]
                + "/"
                + obj.birth_date[4:6]
                + "/"
                + obj.birth_date[6:]
            )
        except:
            obj.birth_date
