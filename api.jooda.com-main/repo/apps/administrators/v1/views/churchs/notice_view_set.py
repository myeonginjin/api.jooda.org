from django.utils.decorators import method_decorator

from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.decorators import action

from common import enums, response, decorators
from common.pagination import JoodaPagination
from common.send import notification

from apps.administrators.v1 import serializers, utils
from apps.churchs.models import ChurchNotice


class ChurchNoticePagination(JoodaPagination):
    default_limit = 7


class ChurchNoticeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    http_method_names = ["get", "post", "patch"]
    pagination_class = ChurchNoticePagination

    @method_decorator(decorators.administrator_authorization())
    def list(self, request):
        administrator = request.administrator
        payload = {}
        try:
            church_notice = (
                ChurchNotice.objects.select_related("church")
                .filter(church=administrator.church)
                .order_by("-created_at")
            )

            paginate_church_notice = self.paginate_queryset(church_notice)
            paginate_church_notice = serializers.ChurchNoticeSerializer(
                paginate_church_notice, many=True
            ).data
            payload["church_notice_list"] = self.get_paginated_response(
                paginate_church_notice
            )

            return response.JoodaResponse.success_response(payload)
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.administrator_authorization())
    def create(self, request):
        administrator = request.administrator
        title = request.data.get("title", None)
        content = request.data.get("content", None)
        image = request.FILES.get("image", None)

        try:
            if not (title and content):
                return response.JoodaResponse.warning_response(request)

            notice = ChurchNotice.objects.create(
                church=administrator.church,
                writer=administrator,
                title=title,
                content=content,
                image=image,
            )

            tokens, accounts = utils.get_id_fcmtoken_from_church(administrator.church)
            notifications = notification.PushNotification(
                tokens=tokens,
                accounts=accounts,
                title=administrator.church.name,
                sub_title=title,
                _id=f"{notice.id}",
                _type=enums.PushNotificationType.NOTICE,
                domain=enums.PushNotificationDomain.CHURCH,
                church_id=str(administrator.church.id),
            )
            notifications.send_push()

            return response.JoodaResponse.success_response()
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.get_object_from_request_id(ChurchNotice))
    @method_decorator(decorators.administrator_authorization())
    def patch(self, request):
        administrator = request.administrator
        church_notice = request.church_notice
        title = request.data.get("title", None)
        content = request.data.get("content", None)
        image = request.FILES.get("image", None)
        is_delete_image = request.data.get("is_delete_image", None)

        try:
            if administrator.church != church_notice.church:
                return response.JoodaResponse.warning_response(
                    request, enums.ErrorCode.FORBIDDEN
                )

            if title is not None:
                church_notice.title = title
            if content is not None:
                church_notice.content = content

            if is_delete_image is not None:
                church_notice.image = None
            elif image:
                church_notice.image = image

            church_notice.save(update_fields=["title", "content", "image"])

            return response.JoodaResponse.success_response()
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.get_object_from_request_id(ChurchNotice))
    @method_decorator(decorators.administrator_authorization())
    @action(detail=False, methods=["post"])
    def delete(self, request):
        administrator = request.administrator
        church_notice = request.church_notice

        try:
            if administrator.church != church_notice.church:
                return response.JoodaResponse.warning_response(
                    request, enums.ErrorCode.FORBIDDEN
                )

            church_notice.delete()

            return response.JoodaResponse.success_response()
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)
