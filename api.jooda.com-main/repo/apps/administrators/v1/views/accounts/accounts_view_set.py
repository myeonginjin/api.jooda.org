from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.decorators import action

from common import enums, response
from common.utils import secure

from apps.administrators.models import Administrator
from apps.administrators.v1 import serializers
from apps.administrators.v1 import utils


class AccountsViewSet(mixins.CreateModelMixin, GenericViewSet):
    http_method_names = ["get", "post"]
    queryset = Administrator.objects.all()

    def create(self, request):
        login_id = request.data.get("id", None)
        password = request.data.get("password", None)
        phone_number = request.data.get("phone_number", None)

        if not (login_id and password and phone_number):
            return response.JoodaResponse.warning_response(request)
        try:
            if self.queryset.filter(login_id=login_id).exists():
                return response.JoodaResponse.warning_response(
                    request, enums.ErrorCode.DUPLICATED_KEY
                )

            Administrator.objects.create(
                login_id=login_id,
                password=secure.encrypte_data(password),
                phone_number=phone_number,
            )
            return response.JoodaResponse.success_response()
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @action(detail=False, methods=["post"])
    def login(self, request):
        login_id = request.data.get("id", None)
        password = request.data.get("password", None)

        payload = {}

        try:
            if not (login_id and password):
                return response.JoodaResponse.warning_response(request)

            administrator = Administrator.objects.get(
                login_id=login_id,
                password=secure.encrypte_data(password),
            )
            authorization_token = utils.create_authorization(login_id)

            administrator.authorization_token = authorization_token
            administrator.save(update_fields=["authorization_token"])

            payload["admin_account_info"] = serializers.AccountInfoSerializer(
                administrator, context={"authorization_token": authorization_token}
            ).data

            return response.JoodaResponse.success_response(payload)
        except Administrator.DoesNotExist:
            return response.JoodaResponse.warning_response(
                request, enums.ErrorCode.FORBIDDEN
            )
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)
