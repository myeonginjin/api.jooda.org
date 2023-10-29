from django.utils.decorators import method_decorator

from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.decorators import action

from common import enums, decorators, response
from common.utils import validate

from apps.administrators.v1 import serializers as serializers
from apps.churchs.models import ChurchWorshipSchedule


class ChurchWorshipScheduleViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    http_method_names = ["get", "post", "patch", "delete"]

    @method_decorator(decorators.administrator_authorization())
    def list(self, request):
        administrator = request.administrator
        payload = {}
        try:
            church_worship_schedule = (
                ChurchWorshipSchedule.objects.select_related("church")
                .filter(church=administrator.church)
                .order_by("weekday", "title", "subtitle")
            )
            payload[
                "worship_schedule_list"
            ] = serializers.ChurchWorshipScheduleSerializer(
                church_worship_schedule, many=True
            ).data

            return response.JoodaResponse.success_response(payload)

        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.administrator_authorization())
    def create(self, request):
        administrator = request.administrator
        title = request.data.get("title", None)
        subtitle = request.data.get("subtitle", None)
        weekday = request.data.get("weekday", None)
        place = request.data.get("place", None)
        mc = request.data.get("mc", None)
        target = request.data.get("target", None)
        reference = request.data.get("reference", None)
        start_time = request.data.get("start_time", None)
        end_time = request.data.get("end_time", None)

        try:
            if not (title and weekday and start_time):
                return response.JoodaResponse.warning_response(request)
            weekday = int(weekday)
            start_time, end_time = validate.validate_time(start_time, end_time)
            if not start_time:
                raise ValueError

            ChurchWorshipSchedule.objects.create(
                church=administrator.church,
                title=title,
                subtitle=subtitle,
                weekday=weekday,
                place=place,
                mc=mc,
                target=target,
                reference=reference,
                start_time=start_time,
                end_time=end_time,
            )

            return response.JoodaResponse.success_response()

        except ValueError:
            return response.JoodaResponse.warning_response(
                request, enums.ErrorCode.BAD_PARAMETER_RECEIVED
            )
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.get_object_from_request_id(ChurchWorshipSchedule))
    @method_decorator(decorators.administrator_authorization())
    def patch(self, request):
        administrator = request.administrator
        church_worship_schedule = request.church_worship_schedule
        title = request.data.get("title", None)
        subtitle = request.data.get("subtitle", None)
        weekday = request.data.get("weekday", None)
        place = request.data.get("place", None)
        mc = request.data.get("mc", None)
        target = request.data.get("target", None)
        reference = request.data.get("reference", None)
        start_time = request.data.get("start_time", None)
        end_time = request.data.get("end_time", None)

        try:
            if administrator.church != church_worship_schedule.church:
                return response.JoodaResponse.warning_response(
                    request, enums.ErrorCode.FORBIDDEN
                )
            if title:
                church_worship_schedule.title = title
            if subtitle is not None:
                church_worship_schedule.subtitle = subtitle
            if weekday:
                weekday = int(weekday)
                if weekday == 6:
                    weekday = -1
                church_worship_schedule.weekday = weekday
            if place is not None:
                church_worship_schedule.place = place
            if mc is not None:
                church_worship_schedule.mc = mc
            if target is not None:
                church_worship_schedule.target = target
            if reference is not None:
                church_worship_schedule.reference = reference
            if start_time:
                church_worship_schedule.start_time = start_time
            if end_time == "":
                church_worship_schedule.end_time = None
            elif end_time and end_time > start_time:
                church_worship_schedule.end_time = end_time

            church_worship_schedule.save(
                update_fields=[
                    "title",
                    "subtitle",
                    "weekday",
                    "place",
                    "mc",
                    "target",
                    "reference",
                    "start_time",
                    "end_time",
                ]
            )

            return response.JoodaResponse.success_response()
        except ValueError:
            return response.JoodaResponse.warning_response(
                request, enums.ErrorCode.BAD_PARAMETER_RECEIVED
            )
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.get_object_from_request_id(ChurchWorshipSchedule))
    @method_decorator(decorators.administrator_authorization())
    @action(detail=False, methods=["post"])
    def delete(self, request):
        administrator = request.administrator
        church_worship_schedule = request.church_worship_schedule
        try:
            if administrator.church != church_worship_schedule.church:
                return response.JoodaResponse.warning_response(
                    request, enums.ErrorCode.FORBIDDEN
                )
            church_worship_schedule.delete()

            return response.JoodaResponse.success_response()
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)
