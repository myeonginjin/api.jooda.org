from django.utils.decorators import method_decorator
from rest_framework.viewsets import mixins, GenericViewSet
from common import response, decorators, enums
from apps.churchs.models import ChurchMember
from common.api.v1 import serializers


class InitViewSet(mixins.ListModelMixin, GenericViewSet):
    @method_decorator(decorators.account_autorization())
    def list(self, request):
        """
        # 앱 접속 API
        """
        payload = {}
        account = request.account
        fcm_token = request.query_params.get("fcm_token", None)

        try:
            if account and fcm_token:
                account.fcm_token = fcm_token
                account.save(update_fields=["fcm_token"])

            church_member = ChurchMember.objects.filter(account=account).exclude(
                state=enums.ChurchMemberState.REJECT
            )
            payload = serializers.InitSerializer(account, church_member)

            return response.JoodaResponse.success_response(payload)
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)
