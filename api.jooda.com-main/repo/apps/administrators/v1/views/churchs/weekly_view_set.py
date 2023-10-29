from django.utils.decorators import method_decorator

from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.decorators import action

from common import enums, response, decorators
from common.pagination import JoodaPagination
from common.utils import validate
from common.send import notification

from apps.churchs.models import ChurchWeekly
from apps.administrators.v1 import serializers, utils
from datetime import datetime


class ChurchWeeklyPagination(JoodaPagination):
    default_limit = 6


class ChurchWeeklyViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet
):
    http_method_names = ["get", "post", "patch"]
    pagination_class = ChurchWeeklyPagination

    @method_decorator(decorators.administrator_authorization())
    def list(self, request):
        administrator = request.administrator
        payload = {}
        try:
            church_weekly = (
                ChurchWeekly.objects.select_related("church")
                .filter(church=administrator.church)
                .order_by("-created_at")
            )
            paginate_church_weekly = self.paginate_queryset(church_weekly)
            paginate_church_weekly = serializers.ChurchWeeklySerializer(
                paginate_church_weekly, many=True
            ).data
            payload["church_weekly_list"] = self.get_paginated_response(
                paginate_church_weekly
            )

            return response.JoodaResponse.success_response(payload)
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.administrator_authorization())
    def create(self, request):
        today = datetime.today()
        administrator = request.administrator
        title = request.data.get("title", None)
        image = request.FILES.get("image", None)
        year = request.data.get("year", str(today.year))
        month = request.data.get("month", str(today.month))

        try:
            if not (title and image):
                return response.JoodaResponse.warning_response(request)
            year, month, _ = validate.validate_date(year, month, "01")

            weekly = ChurchWeekly.objects.create(
                church=administrator.church,
                title=title,
                image=image,
                year=year,
                month=month,
            )

            tokens, accounts = utils.get_id_fcmtoken_from_church(administrator.church)
            notifications = notification.PushNotification(
                tokens=tokens,
                accounts=accounts,
                title=administrator.church.name,
                sub_title=title,
                _id=f"{weekly.id}",
                _type=enums.PushNotificationType.WEEKLY,
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

    @method_decorator(decorators.get_object_from_request_id(ChurchWeekly))
    @method_decorator(decorators.administrator_authorization())
    def patch(self, request):
        administrator = request.administrator
        church_weekly = request.church_weekly
        title = request.data.get("title", None)
        image = request.FILES.get("image", None)
        year = request.data.get("year", None)
        month = request.data.get("month", None)

        try:
            if administrator.church != church_weekly.church:
                return response.JoodaResponse.warning_response(
                    request, enums.ErrorCode.FORBIDDEN
                )

            if title is not None:
                church_weekly.title = title

            if image:
                church_weekly.image = image

            if year and month:
                church_weekly.year = year
                church_weekly.month = month

            church_weekly.save(update_fields=["title", "image", "year", "month"])

            return response.JoodaResponse.success_response()
        except ValueError:
            return response.JoodaResponse.warning_response(
                request, enums.ErrorCode.BAD_PARAMETER_RECEIVED
            )
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.get_object_from_request_id(ChurchWeekly))
    @method_decorator(decorators.administrator_authorization())
    @action(detail=False, methods=["post"])
    def delete(self, request):
        administrator = request.administrator
        church_weekly = request.church_weekly

        try:
            if administrator.church != church_weekly.church:
                return response.JoodaResponse.warning_response(
                    request, enums.ErrorCode.FORBIDDEN
                )

            church_weekly.delete()

            return response.JoodaResponse.success_response()
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)
