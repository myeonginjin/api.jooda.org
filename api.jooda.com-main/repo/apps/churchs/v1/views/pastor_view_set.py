from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from django.db.models import Avg
from rest_framework.viewsets import mixins, GenericViewSet
from apps.churchs.models import Church, ChurchPastor
from apps.churchs.v1 import serializers
from common import response, pagination, decorators


class ChurchPastorPagination(pagination.JoodaPagination):
    default_limit = 12


class ChurchPastorViewSet(mixins.ListModelMixin, GenericViewSet):
    pagination_class = ChurchPastorPagination

    @method_decorator(decorators.account_autorization())
    @method_decorator(decorators.get_object_from_request_id(Church))
    def list(self, request):
        """
        # 교회 섬기는 이 리스트 API
        """

        payload = {}
        church = request.church
        role = request.query_params.get("role", None)
        try:
            pastors = ChurchPastor.objects.filter(church=church).order_by("order")
            if role:
                pastors = pastors.filter(role=role)

            paginate_pastors = self.paginate_queryset(pastors)
            paginate_pastors = serializers.ChurchPastorsSerializer(
                paginate_pastors, many=True
            ).data

            payload["pastors_list"] = self.get_paginated_response(paginate_pastors)

            return response.JoodaResponse.success_response(payload)

        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.account_autorization())
    @method_decorator(decorators.get_object_from_request_id(Church))
    @action(detail=False, methods=["get"])
    def role(self, request):
        """
        # 교회 직분 리스트 API
        """

        payload = {}
        church = request.church

        try:
            role_list = (
                ChurchPastor.objects.filter(church=church)
                .values_list("role", flat=True)
                .annotate(avg=Avg("order"))
                .order_by("avg")
            )
            payload["role_list"] = role_list

            return response.JoodaResponse.success_response(payload)

        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)
