from django.utils.decorators import method_decorator
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.decorators import action
from common import response, decorators, format
from apps.churchs.models import Church, ChurchCalendar
from datetime import date, timedelta, datetime
from apps.churchs.v1 import serializers
from calendar import monthrange


class ChurchCalendarViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet
):
    @method_decorator(decorators.account_autorization())
    @method_decorator(decorators.get_object_from_request_id(Church))
    def list(self, request):
        """
        # 교회 달력 리스트 API
        """

        payload = {}
        church = request.church
        today = date.today()
        year = request.query_params.get("year", str(today.year))
        month = request.query_params.get("month", format.month(today.month))

        try:
            year = int(year)
            month = int(month)

            first_day_of_month = date(year, month, 1)
            last_day_of_month = date(year, month, monthrange(year, month)[1])

            min_date_range = first_day_of_month - timedelta(days=6)
            max_date_range = last_day_of_month + timedelta(days=6)

            church_calendar = (
                ChurchCalendar.objects.select_related("church")
                .filter(
                    church=church,
                    start_date__lte=max_date_range,
                    end_date__gte=min_date_range,
                )
                .order_by("start_date")
            )

            payload["church_calendar_list"] = serializers.ChurchCalendarListSerializer(
                church_calendar, many=True
            ).data

            return response.JoodaResponse.success_response(payload)

        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.account_autorization())
    @method_decorator(decorators.get_object_from_request_id(ChurchCalendar))
    def retrieve(self, request, pk=None):
        """
        # 교회 달력 세부 API
        """

        payload = {}
        church_calendar = request.church_calendar
        try:
            payload[
                "church_calendar_detail"
            ] = serializers.ChurchCalendarDetailSerializer(church_calendar).data

            return response.JoodaResponse.success_response(payload)
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)
