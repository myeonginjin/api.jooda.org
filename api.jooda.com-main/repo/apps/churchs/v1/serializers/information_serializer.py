from rest_framework import serializers
from apps.churchs.models import Church, ChurchMember
from common import enums, slack


class ChurchInformationSerializer(serializers.ModelSerializer):
    church_id = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()
    denomination_name = serializers.SerializerMethodField()
    member_state = serializers.SerializerMethodField()

    class Meta:
        model = Church
        fields = (
            "church_id",
            "name",
            "member_count",
            "denomination_name",
            "introduction_title",
            "introduction_content",
            "address",
            "thumbnail",
            "logo",
            "member_state",
        )

    def get_church_id(self, obj):
        return obj.id

    def get_church_id(self, obj):
        return obj.id

    def get_member_count(self, obj):
        return f"{obj.church_member.count():,}"

    def get_denomination_name(self, obj):
        if obj.denomination:
            return obj.denomination.name
        return ""

    def get_member_state(self, obj):
        account = self.context["account"]
        try:
            return obj.church_member.filter(account=account).get().state

        except ChurchMember.MultipleObjectsReturned:
            slacks = slack.Slack(enums.SlackChannel.ERROR_LOG)
            slacks.slack_post_texts(
                f"❗️긴급❗️[ChurchMember] account : {account} church : {obj} 🧑🏾‍⚖️ 중복되는 객체가 있습니다. 1개만 남겨주세요"
            )
            return enums.ChurchMemberState.VISITOR

        except:
            return enums.ChurchMemberState.VISITOR
