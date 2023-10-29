from django.utils.decorators import method_decorator

from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.decorators import action

from common import response, enums, decorators
from common.pagination import JoodaPagination
from common.utils import json_parsers, validate

from apps.churchs.models import ChurchHistory
from apps.administrators.v1 import serializers


class ChurchHistoryPagination(JoodaPagination):
    default_limit = 12


class ChurchHistoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    http_method_names = ["get", "post", "patch"]
    pagination_class = ChurchHistoryPagination

    @method_decorator(decorators.administrator_authorization())
    def list(self, request):
        administrator = request.administrator
        payload = {}
        try:
            church_histoies = (
                ChurchHistory.objects.select_related("church")
                .filter(church=administrator.church)
                .order_by("-year", "-month", "-day")
            )
            paginate_church_histoies = self.paginate_queryset(church_histoies)
            paginate_church_histoies = serializers.ChurchHistorySerializer(
                paginate_church_histoies, many=True
            ).data
            payload["church_history_list"] = self.get_paginated_response(
                paginate_church_histoies
            )

            return response.JoodaResponse.success_response(payload)
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.administrator_authorization())
    def create(self, request):
        administrator = request.administrator
        history_list = [
            json_parsers.request_data_to_json(data)
            for data in request.data.getlist("history_list", None)
        ]
        church_histories = []

        try:
            if not history_list:
                return response.JoodaResponse.warning_response(request)

            for history in history_list:
                year, month, day = validate.validate_date(
                    history.get("year", None),
                    history.get("month", None),
                    history.get("day", None),
                )
                church_histories.append(
                    ChurchHistory(
                        church=administrator.church,
                        year=year,
                        month=month,
                        day=day,
                        content=history.get("content", None),
                    )
                )

            ChurchHistory.objects.bulk_create(church_histories)
            return response.JoodaResponse.success_response()

        except ValueError:
            return response.JoodaResponse.warning_response(
                request, enums.ErrorCode.BAD_PARAMETER_RECEIVED
            )
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.administrator_authorization())
    def patch(self, request):
        administrator = request.administrator
        history_list = [
            json_parsers.request_data_to_json(data)
            for data in request.data.getlist("history_list", None)
        ]

        try:
            if not history_list:
                return response.JoodaResponse.warning_response(request)

            history_id_list = [
                history.get("church_history_id", None) for history in history_list
            ]
            church_histories = ChurchHistory.objects.filter(
                id__in=history_id_list,
                church=administrator.church,
            ).order_by("id")

            for index, church_history in enumerate(church_histories):
                year, month, day, content = json_parsers.find_values_to_json_list(
                    json_list=history_list,
                    id_list=history_id_list,
                    index=index,
                    key="history_id",
                    id=str(church_history.id),
                    output_keys=["year", "month", "day", "content"],
                )
                print(year, month, day, content)

                if year or month or day:
                    year, month, day = validate.validate_date(
                        year if year else church_history.year,
                        month if month else church_history.month,
                        day if day else church_history.day,
                    )
                    church_history.year = year
                    church_history.month = month
                    church_history.day = day
                if content:
                    church_history.content = content

            ChurchHistory.objects.bulk_update(
                church_histories, ["year", "month", "day", "content"]
            )
            return response.JoodaResponse.success_response()

        except ValueError as v:
            print(v)
            return response.JoodaResponse.warning_response(
                request, enums.ErrorCode.BAD_PARAMETER_RECEIVED
            )
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @action(detail=False, methods=["post"])
    @method_decorator(decorators.administrator_authorization())
    def delete(self, request):
        administrator = request.administrator
        history_list = request.data.getlist("history_list", None)

        try:
            if not history_list:
                return response.JoodaResponse.warning_response(request)
            church_histories = ChurchHistory.objects.filter(
                church=administrator.church,
                id__in=history_list,
            )
            church_histories._raw_delete(church_histories.db)
            return response.JoodaResponse.success_response()
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)
