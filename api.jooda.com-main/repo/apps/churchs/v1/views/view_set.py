from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.viewsets import mixins, GenericViewSet
from apps.churchs.models import Church, ChurchMember
from apps.churchs.v1 import serializers
from common import response, decorators, enums, slack


class ChurchViewSet(mixins.ListModelMixin, GenericViewSet):
    @method_decorator(decorators.account_autorization())
    def list(self, request):
        """
        # 교회 리스트 API
        """
        payload = {}

        try:
            churchs = Church.objects.all()
            payload["church_list"] = serializers.ChurchListSerializer(
                churchs, many=True
            ).data

            return response.JoodaResponse.success_response(payload)

        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.account_autorization())
    @method_decorator(decorators.get_object_from_request_id(Church))
    @action(detail=False, methods=["get"])
    def information(self, request):
        """
        # 교회 정보 API
        """

        payload = {}
        church = request.church
        account = request.account

        try:
            payload["church_information"] = serializers.ChurchInformationSerializer(
                church, context={"account": account}
            ).data
            return response.JoodaResponse.success_response(payload)
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.account_autorization())
    @method_decorator(decorators.get_object_from_request_id(Church))
    @action(detail=False, methods=["get"])
    def introduction(self, request):
        """
        # 교회 소개 API
        """

        payload = {}
        church = request.church

        try:
            payload["church_introduction"] = serializers.ChurchIntroductionSerializer(
                church
            ).data

            return response.JoodaResponse.success_response(payload)

        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.account_autorization())
    @method_decorator(decorators.get_object_from_request_id(Church))
    @action(detail=False, methods=["post"])
    def register(self, request):
        """
        # 교회 등록 API
        """

        church = request.church
        account = request.account

        try:
            churhch_member = ChurchMember.objects.filter(
                church=church, account=account
            ).get()

            if churhch_member:
                churhch_member.state = enums.ChurchMemberState.CONFIRM
                churhch_member.save(update_fields=["state"])

            return response.JoodaResponse.success_response()

        except ChurchMember.DoesNotExist:
            ChurchMember.objects.create(church=church, account=account)
            return response.JoodaResponse.success_response()

        except ChurchMember.MultipleObjectsReturned:
            slacks = slack.Slack(enums.SlackChannel.ERROR_LOG)
            slacks.slack_post_texts(
                f"❗️긴급❗️[ChurchMember] account : {account} church : {church} 🧑🏾‍⚖️ 중복되는 객체가 있습니다. 1개만 남겨주세요"
            )

            return response.JoodaResponse.success_response()

        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.account_autorization())
    @method_decorator(decorators.get_object_from_request_id(Church))
    @action(detail=False, methods=["post"])
    def delete(self, request):
        """
        # 교회 삭제 API
        """

        church = request.church
        account = request.account

        try:
            churhch_member = ChurchMember.objects.get(church=church, account=account)
            churhch_member.delete()

            return response.JoodaResponse.success_response()

        except ChurchMember.DoesNotExist:
            return response.JoodaResponse.warning_response(
                request, church=church, account=account
            )

        except ChurchMember.MultipleObjectsReturned:
            ChurchMember.objects.filter(church=church, account=account).delete()
            return response.JoodaResponse.success_response()

        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)
