from django.utils.decorators import method_decorator
from rest_framework.viewsets import mixins, GenericViewSet
from common import decorators, response
from apps.churchs.v1 import serializers
from apps.churchs.models import Church, ChurchWorshipSchedule


class ChurchWorshipScheduleViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet
):
    @method_decorator(decorators.account_autorization())
    @method_decorator(decorators.get_object_from_request_id(Church))
    def list(self, request):
        """
        # 교회 예배 일정 리스트 API
        """
        payload = {}
        church = request.church

        try:
            church_worship_schedule_list = (
                ChurchWorshipSchedule.objects.select_related("church")
                .filter(church=church)
                .order_by(
                    "weekday",
                    "title",
                    "subtitle",
                )
            )

            payload = serializers.ChurchWorshipScheduleListSerializer(
                church_worship_schedule_list
            )

            return response.JoodaResponse.success_response(payload)

        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.account_autorization())
    @method_decorator(decorators.get_object_from_request_id(ChurchWorshipSchedule))
    def retrieve(self, request, pk=None):
        """
        # 교회 예배 일정 세부 API
        """

        payload = {}
        church_worship_schedule = request.church_worship_schedule
        try:
            payload[
                "church_worship_schedule_detail"
            ] = serializers.ChurchWorshipScheduleDetailSerializer(
                church_worship_schedule
            ).data

            return response.JoodaResponse.success_response(payload)
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)
