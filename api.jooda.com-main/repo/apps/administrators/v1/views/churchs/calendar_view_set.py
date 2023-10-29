from django.utils.decorators import method_decorator


from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.decorators import action


from common import enums, decorators, response, format
from common.utils import validate
from common.send import notification

from apps.churchs.models import ChurchCalendar
from apps.administrators.v1 import serializers, utils

from datetime import date, timedelta, datetime
from calendar import monthrange

from calendar import monthrange
from datetime import datetime, timedelta


class ChurchCalendarViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    http_method_names = ["get", "post", "patch", "delete"]

    @method_decorator(decorators.administrator_authorization())
    def list(self, request):
        today = datetime.today()
        administrator = request.administrator
        year = request.query_params.get("year", str(today.year))
        month = request.query_params.get("month", format.month(today.month))
        payload = {}
        try:
            one_week = timedelta(days=7)
            start_date = datetime(int(year), int(month), 1) - one_week
            end_date = (
                datetime(
                    int(year),
                    int(month),
                    monthrange(int(year), int(month))[1],
                )
                + one_week
            )
            church_calendar = (
                ChurchCalendar.objects.select_related("church")
                .filter(
                    church=administrator.church,
                    start_date__lte=end_date,
                    end_date__gte=start_date,
                )
                .order_by("start_date")
            )
            payload["church_calendar_list"] = serializers.ChurchCalendarSerializer(
                church_calendar,
                context={"month": month},
                many=True,
            ).data

            return response.JoodaResponse.success_response(payload)

        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.administrator_authorization())
    def create(self, request):
        administrator = request.administrator
        title = request.data.get("title", None)
        content = request.data.get("content", None)
        start_date = request.data.get("start_date", None)
        end_date = request.data.get("end_date", None)

        try:
            if not (title and start_date):
                return response.JoodaResponse.warning_response(request)

            start_date, end_date = validate.validate_start_end_date(
                start_date, end_date
            )

            if not (start_date):
                raise ValueError

            calendar = ChurchCalendar.objects.create(
                church=administrator.church,
                title=title,
                content=content,
                start_date=start_date,
                end_date=end_date,
            )

            tokens, accounts = utils.get_id_fcmtoken_from_church(administrator.church)
            notifications = notification.PushNotification(
                tokens=tokens,
                accounts=accounts,
                title=administrator.church.name,
                sub_title=title,
                _id=f"{calendar.id}",
                _type=enums.PushNotificationType.CALENDAR,
                domain=enums.PushNotificationDomain.CHURCH,
                church_id=str(administrator.church.id),
            )
            notifications.send_push()

            return response.JoodaResponse.success_response()
        except ValueError:
            return response.JoodaResponse.warning_response(
                request, enums.ErrorCode.BAD_PARAMETER_RECEIVED
            )
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.get_object_from_request_id(ChurchCalendar))
    @method_decorator(decorators.administrator_authorization())
    def patch(self, request):
        administrator = request.administrator
        church_calendar = request.church_calendar
        title = request.data.get("title", None)
        content = request.data.get("content", None)
        start_date = request.data.get("start_date", None)
        end_date = request.data.get("end_date", None)

        try:
            if administrator.church != church_calendar.church:
                return response.JoodaResponse.warning_response(
                    request, enums.ErrorCode.FORBIDDEN
                )

            if title:
                church_calendar.title = title
            if content is not None:
                church_calendar.content = content
            if start_date or end_date:
                if start_date and not end_date:
                    end_date = str(church_calendar.end_date)
                elif not start_date and end_date:
                    start_date = str(church_calendar.start_date)
                start_date, end_date = validate.validate_start_end_date(
                    start_date, end_date
                )
                if not (start_date):
                    raise ValueError

                church_calendar.start_date = start_date
                church_calendar.end_date = end_date

            church_calendar.save(
                update_fields=["title", "content", "start_date", "end_date"]
            )
            return response.JoodaResponse.success_response()
        except ValueError:
            return response.JoodaResponse.warning_response(
                request, enums.ErrorCode.BAD_PARAMETER_RECEIVED
            )
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.get_object_from_request_id(ChurchCalendar))
    @method_decorator(decorators.administrator_authorization())
    @action(detail=False, methods=["post"])
    def delete(self, request):
        administrator = request.administrator
        church_calendar = request.church_calendar
        try:
            if administrator.church != church_calendar.church:
                return response.JoodaResponse.warning_response(
                    request, enums.ErrorCode.FORBIDDEN
                )
            church_calendar.delete()

            return response.JoodaResponse.success_response()
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)
