from django.utils.decorators import method_decorator
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.decorators import action
from common import response, pagination, decorators
from apps.churchs.models import Church, ChurchNotice
from apps.churchs.v1 import serializers


class ChurchNoticePagination(pagination.JoodaPagination):
    default_limit = 15


class ChurchNoticeViewset(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet
):
    pagination_class = ChurchNoticePagination

    @method_decorator(decorators.account_autorization())
    @method_decorator(decorators.get_object_from_request_id(Church))
    def list(self, request):
        """
        # 교회 공지사항 리스트 API
        """
        payload = {}
        church = request.church

        try:
            church_notice_list = (
                ChurchNotice.objects.select_related("church")
                .filter(church=church)
                .order_by("-created_at")
            )

            paginate_church_notice_list = self.paginate_queryset(church_notice_list)

            paginate_church_notice_list = serializers.ChurchNoticeListSerializer(
                paginate_church_notice_list, many=True
            ).data

            payload["church_notice_list"] = self.get_paginated_response(
                paginate_church_notice_list
            )

            return response.JoodaResponse.success_response(payload)

        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.account_autorization())
    @method_decorator(decorators.get_object_from_request_id(ChurchNotice))
    def retrieve(self, request, pk=None):
        """
        # 교회 공지사항 세부 API
        """

        payload = {}
        church_notice = request.church_notice

        try:
            payload["church_notice_detail"] = serializers.ChurchNoticeDetailSerializer(
                church_notice
            ).data

            return response.JoodaResponse.success_response(payload)
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)
