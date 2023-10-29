from django.utils.decorators import method_decorator
from apps.churchs.v1 import serializers
from rest_framework.viewsets import mixins, GenericViewSet
from apps.churchs.models import Church, ChurchHistory
from common import response, pagination, decorators


class ChurchHistoryPagination(pagination.JoodaPagination):
    default_limit = 20


class ChurchHistoryViewSet(mixins.ListModelMixin, GenericViewSet):
    pagination_class = ChurchHistoryPagination

    @method_decorator(decorators.account_autorization())
    @method_decorator(decorators.get_object_from_request_id(Church))
    def list(self, request):
        """
        # 교회 연혁 리스트 API
        """
        payload = {}
        church = request.church

        try:
            church_history_list = (
                ChurchHistory.objects.select_related("church")
                .filter(church=church)
                .order_by("-year", "-month", "-day")
            )

            paginate_church_history_list = self.paginate_queryset(church_history_list)

            paginate_church_history_list = serializers.ChurchHistorySerializer(
                paginate_church_history_list, many=True
            ).data

            payload["church_history_list"] = self.get_paginated_response(
                paginate_church_history_list
            )

            return response.JoodaResponse.success_response(payload)

        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)
