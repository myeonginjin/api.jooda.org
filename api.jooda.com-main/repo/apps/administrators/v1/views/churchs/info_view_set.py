from django.utils.decorators import method_decorator
from django.db import transaction
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.decorators import action

from common import enums, slack, response, decorators
from common.utils import geocoding

from apps.administrators.v1 import utils, serializers
from apps.administrators.models import Administrator
from apps.churchs.models import Church, ChurchDenomination, ChurchDirections


class ChurchInfoViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet
):
    http_method_names = ["list", "get", "post", "patch"]
    queryset = Administrator.objects.all()

    @method_decorator(decorators.administrator_authorization())
    def list(self, request):
        administrator = request.administrator
        payload = {}
        try:
            church = administrator.church
            if not church:
                raise ValueError

            denomination_list = list(
                ChurchDenomination.objects.values_list("name", flat=True).all()
            )

            payload["church_info"] = serializers.ChurchInfoSerializer(
                church, context={"denomination_list": denomination_list}
            ).data

            return response.JoodaResponse.success_response(payload)

        except ValueError:
            return response.JoodaResponse.warning_response(
                request, enums.ErrorCode.FORBIDDEN
            )
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.administrator_authorization())
    def create(self, request):
        administrator = request.administrator
        church_name = request.data.get("church_name", None)
        contact_number = request.data.get("contact_number", None)
        denomination_name = request.data.get("denomination_name", None)
        introduction_title = request.data.get("introduction_title", None)
        introduction_content = request.data.get("introduction_content", None)
        address = request.data.get("address", None)
        detail_address = request.data.get("detail_address", None)
        thumbnail = request.FILES.get("thumbnail", None)
        logo = request.FILES.get("logo", None)

        payload = {}

        try:
            if administrator.church != None or not (
                church_name and contact_number and address
            ):
                return response.JoodaResponse.warning_response(request)
            new_church = Church.objects.create(
                name=church_name,
                contact_number=contact_number,
                address=address,
                detail_address=detail_address,
                thumbnail=thumbnail,
                logo=logo,
                introduction_title=introduction_title,
                introduction_content=introduction_content,
            )
            administrator.church = new_church
            administrator.save(update_fields=["church"])

            payload["admin_account_info"] = serializers.AccountInfoSerializer(
                administrator
            ).data

            utils.resigter_denomination(new_church, denomination_name)

            slack_attachment = slack.SlackAttachments(
                enums.SlackChannel.REQUEST_REGISTERING_CHURCH
            )
            slack_attachment.request_registering_church(new_church)

            return response.JoodaResponse.success_response(payload)
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.administrator_authorization())
    def patch(self, request):
        administrator = request.administrator
        church_name = request.data.get("church_name", None)
        contact_number = request.data.get("contact_number", None)
        denomination_name = request.data.get("denomination_name", None)
        introduction_title = request.data.get("introduction_title", None)
        introduction_content = request.data.get("introduction_content", None)
        address = request.data.get("address", None)
        detail_address = request.data.get("detail_address", None)
        is_delete_thumbnail = request.data.get("is_delete_thumbnail", None)
        thumbnail = request.FILES.get("thumbnail", None)
        is_delete_logo = request.data.get("is_delete_logo", None)
        logo = request.FILES.get("logo", None)

        try:
            church = administrator.church
            utils.resigter_denomination(church, denomination_name)
            if church_name:
                church.name = church_name
            if contact_number:
                church.contact_number = contact_number
            if introduction_title is not None:
                church.introduction_title = introduction_title
            if introduction_content is not None:
                church.introduction_content = introduction_content
            if address:
                church.address = address
                (
                    church.longitude,
                    church.latitude,
                ) = geocoding.convert_address_to_coordinate(address)
            if detail_address:
                church.detail_address = detail_address
            if is_delete_thumbnail is not None:
                church.thumbnail = None
            elif thumbnail:
                church.thumbnail = thumbnail
            if is_delete_logo is not None:
                church.logo = None
            elif logo:
                church.logo = logo
            church.save(
                update_fields=[
                    "name",
                    "contact_number",
                    "introduction_title",
                    "introduction_content",
                    "address",
                    "longitude",
                    "latitude",
                    "detail_address",
                    "thumbnail",
                    "logo",
                ]
            )
            return response.JoodaResponse.success_response()
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)
