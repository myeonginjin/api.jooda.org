from django.utils.decorators import method_decorator

from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.decorators import action

from common import enums, response, decorators
from common.pagination import JoodaPagination
from common.utils import json_parsers

from apps.administrators.v1 import utils, serializers
from apps.churchs.models import ChurchPastor


class ChurchPastorPagination(JoodaPagination):
    default_limit = 6


class ChurchPastorViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    http_method_names = ["get", "post", "patch"]
    queryset = ChurchPastor.objects.all()
    pagination_class = ChurchPastorPagination

    @method_decorator(decorators.administrator_authorization())
    def list(self, request):
        administrator = request.administrator
        payload = {}
        try:
            church_pastor = (
                ChurchPastor.objects.select_related("church")
                .filter(church=administrator.church)
                .order_by("order")
            )

            paginate_church_pastor = self.paginate_queryset(church_pastor)
            paginate_church_pastor = serializers.ChurchPastorSerializer(
                paginate_church_pastor, many=True
            ).data
            payload["church_pastor_list"] = self.get_paginated_response(
                paginate_church_pastor
            )

            return response.JoodaResponse.success_response(payload)
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.administrator_authorization())
    def create(self, request):
        administrator = request.administrator
        pastor_list = [
            json_parsers.request_data_to_json(data)
            for data in request.data.getlist("pastor_list", None)
        ]
        image_list = [file for file in request.FILES.getlist("image_list", None)]
        image_index = 0

        new_pastor_list = []

        try:
            if not pastor_list:
                return response.JoodaResponse.warning_response(request)
            current_order = utils.PastorOrder.get_last_order(administrator.church)

            for pastor in pastor_list:
                pastor_image = None
                if pastor.get("image_state", None):
                    pastor_image = image_list[image_index]
                    image_index += 1
                current_order = utils.PastorOrder.get_next_order(current_order)
                new_pastor_list.append(
                    ChurchPastor(
                        church=administrator.church,
                        name=pastor.get("name", None),
                        role=pastor.get("role", None),
                        image=pastor_image,
                        order=current_order,
                    )
                )

            ChurchPastor.objects.bulk_create(new_pastor_list)
            return response.JoodaResponse.success_response()
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.get_object_from_request_id(ChurchPastor))
    @method_decorator(decorators.administrator_authorization())
    def patch(self, request):
        administrator = request.administrator
        church_pastor = request.church_pastor
        name = request.data.get("name", None)
        role = request.data.get("role", None)
        image = request.FILES.get("image", None)
        is_delete_image = request.data.get("is_delete_image", None)

        try:
            if administrator.church != church_pastor.church:
                return response.JoodaResponse.warning_response(
                    request, enums.ErrorCode.FORBIDDEN
                )

            if name is not None:
                church_pastor.name = name
            if role is not None:
                church_pastor.role = role

            if is_delete_image is not None:
                church_pastor.image = None
            elif image:
                church_pastor.image = image

            church_pastor.save(update_fields=["name", "role", "image"])

            return response.JoodaResponse.success_response()
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @action(detail=False, methods=["post"])
    @method_decorator(decorators.get_object_from_request_id(ChurchPastor))
    @method_decorator(decorators.administrator_authorization())
    def delete(self, request):
        administrator = request.administrator
        church_pastor = request.church_pastor

        try:
            if administrator.church != church_pastor.church:
                return response.JoodaResponse.warning_response(
                    request, enums.ErrorCode.FORBIDDEN
                )

            church_pastor.delete()

            return response.JoodaResponse.success_response()
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @action(detail=False, methods=["post"])
    @method_decorator(decorators.get_object_from_request_id(ChurchPastor))
    @method_decorator(decorators.administrator_authorization())
    def change_order(self, request):
        administrator = request.administrator
        church_pastor = request.church_pastor
        index = int(request.data.get("index", -1))

        try:
            if index == -1:
                return response.JoodaResponse.warning_response(request)

            church_pastors = (
                ChurchPastor.objects.select_related("church")
                .filter(church=administrator.church)
                .order_by("order")
            )

            order = utils.PastorOrder.get_changed_order(church_pastors, index)

            if order:
                church_pastor.order = order
                church_pastor.save(update_fields=["order"])
            else:
                utils.PastorOrder.refresh_order(church_pastors, church_pastor, index)

            return response.JoodaResponse.success_response()
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)
