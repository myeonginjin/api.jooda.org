from django.utils.decorators import method_decorator
from apps.churchs.v1 import serializers
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.decorators import action
from apps.churchs.models import Church, ChurchWeekly
from common import response, pagination, decorators
from datetime import datetime


class ChurchWeeklyPagination(pagination.JoodaPagination):
    default_limit = 15


class ChurchWeeklyViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet
):
    pagination_class = ChurchWeeklyPagination

    @method_decorator(decorators.account_autorization())
    @method_decorator(decorators.get_object_from_request_id(Church))
    def list(self, request):
        """
        # 교회 주보 리스트 API
        """

        payload = {}
        church = request.church
        date = request.query_params.get("date", None)

        try:
            if date:
                try:
                    datetime.strptime(f"20{date}", "%Y%m")
                    year = date[0:2]
                    month = date[2:4]
                except:
                    return response.JoodaResponse.warning_response(
                        request, wrong_date=date
                    )

            else:
                year = datetime.now().strftime("%Y")[2:4]
                month = datetime.now().strftime("%m")

            church_weekly_list = (
                ChurchWeekly.objects.select_related("church")
                .filter(church=church, year=year, month=month)
                .order_by("-created_at")
            )

            payload["church_weekly_list"] = serializers.ChurchWeeklyListSerializer(
                church_weekly_list, many=True
            ).data

            return response.JoodaResponse.success_response(payload)

        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.account_autorization())
    @method_decorator(decorators.get_object_from_request_id(ChurchWeekly))
    def retrieve(self, request, pk=None):
        """
        # 교회 주보 세부 API
        """

        payload = {}
        church_weekly = request.church_weekly

        try:
            payload["church_weekly_detail"] = serializers.ChurchWeeklyDetailSerializer(
                church_weekly
            ).data

            return response.JoodaResponse.success_response(payload)
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.account_autorization())
    @method_decorator(decorators.get_object_from_request_id(Church))
    @action(detail=False, methods=["get"])
    def date(self, request):
        """
        # 교회 주보 등록날짜 리스트 API
        """

        payload = {}
        church = request.church

        try:
            date_list = (
                ChurchWeekly.objects.select_related("church")
                .filter(church=church)
                .order_by("-year", "-month")
                .distinct()
                .values_list("year", "month")
            )

            paginate_date_list = self.paginate_queryset(date_list)

            paginate_date_list = (
                serializers.ChurchWeeklyDeteListSerializer.get_date_list(
                    paginate_date_list
                )
            )

            payload["date_list"] = self.get_paginated_response(paginate_date_list)

            return response.JoodaResponse.success_response(payload)
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)
