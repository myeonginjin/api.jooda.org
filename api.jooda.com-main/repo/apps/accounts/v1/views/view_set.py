from django.utils.decorators import method_decorator

from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.decorators import action

from re import sub

from common import response, enums, randoms, decorators, slack
from common.send import message
from common.utils import secure
from apps.accounts.models import Account


class AccountViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    http_method_names = ["get", "post", "patch"]
    queryset = Account.objects.all()

    @method_decorator(decorators.account_autorization())
    @action(detail=False, methods=["post"])
    def message_authentication(self, request):
        phone_number = request.data.get("phone_number", "")
        payload = {}
        try:
            authentication_number = randoms.get_message_authentication_random_number()
            payload["authentication_number"] = authentication_number
            payload["is_duplicated_phone_number"] = Account.objects.filter(
                phone_number=phone_number
            ).exists()

            phone_number = sub("-", "", phone_number)

            message.authentication_message(phone_number, authentication_number)
            return response.JoodaResponse.success_response(payload)
        except ValueError:
            return response.JoodaResponse.warning_response(request)
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.account_autorization())
    def create(self, request):
        name = request.data.get("name", None)
        phone_number = request.data.get("phone_number", None)
        password = request.data.get("password", None)
        gender = request.data.get("gender", None)
        birth_date = request.data.get("birth_date", None)
        os = request.headers.get("os", None)
        device_id = request.headers.get("device-id", None)
        app_version = request.headers.get("app-version", None)
        fcm_token = request.data.get("fcm_token", None)
        inquire = request.data.get("inquire", None)
        payload = {}

        try:
            if not (
                name
                and phone_number
                and password
                and gender
                and birth_date
                and os
                and device_id
                and app_version
            ):
                return response.JoodaResponse.warning_response(
                    request,
                    name=name,
                    phone_number=phone_number,
                    password=password,
                    gender=gender,
                    birth_date=birth_date,
                    os=os,
                    device_id=device_id,
                    app_version=app_version,
                )

            same_phone_number_account = Account.objects.filter(
                phone_number=phone_number
            )
            if same_phone_number_account.count() >= 1:
                if inquire:
                    same_phone_number_account = same_phone_number_account.get()
                    same_phone_number_account.state = enums.AccountState.IN_ACTIVE
                    same_phone_number_account.save(update_fields=["state"])
                else:
                    return response.JoodaResponse.warning_response(
                        request, enums.ErrorCode.DUPLICATED_KEY
                    )

            account = Account.objects.create(
                name=name,
                phone_number=phone_number,
                password=secure.encrypte_data(str(password)),
                gender=gender,
                birth_date=birth_date,
                os=os,
                device_id=f"{os}-{device_id}",
                app_version=app_version,
                fcm_token=fcm_token,
            )

            if inquire:
                account.state = enums.AccountState.WAIT_FOR
                account.save(update_fields=["state"])
                slack_attachment = slack.SlackAttachments(
                    enums.SlackChannel.ACCOUNT_INQUIRE
                )
                slack_attachment.duplicated_phone_number(
                    account, same_phone_number_account
                )

            payload["authorization_token"] = account.id

            return response.JoodaResponse.success_response(payload)
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.account_autorization())
    @action(detail=False, methods=["post"])
    def login(self, request):
        phone_number = request.data.get("phone_number", None)
        password = request.data.get("password", None)

        payload = {}

        try:
            if not (phone_number and password):
                return response.JoodaResponse.warning_response(request)
            account = Account.objects.get(
                phone_number=phone_number,
                password=secure.encrypte_data(str(password)),
            )
            payload["authorization_token"] = account.id

            return response.JoodaResponse.success_response(payload)

        except Account.DoesNotExist:
            return response.JoodaResponse.warning_response(
                request, enums.ErrorCode.FORBIDDEN
            )
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.account_autorization())
    @action(detail=False, methods=["post"])
    def check(self, request):
        name = request.data.get("name", None)
        birth_date = request.data.get("birth_date", None)
        phone_number = request.data.get("phone_number", None)

        payload = {}

        try:
            if not (name and birth_date and phone_number):
                return response.JoodaResponse.warning_response(request)
            account = Account.objects.get(
                name=name,
                birth_date=birth_date,
                phone_number=phone_number,
            )
            payload["authorization_token"] = account.id

            return response.JoodaResponse.success_response(payload)

        except Account.DoesNotExist:
            return response.JoodaResponse.warning_response(
                request, enums.ErrorCode.FORBIDDEN
            )
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.account_autorization())
    def patch(self, request):
        account = request.account
        name = request.data.get("name", None)
        phone_number = request.data.get("phone_number", None)
        password = request.data.get("password", None)
        gender = request.data.get("gender", None)
        birth_date = request.data.get("birth_date", None)
        os = request.headers.get("os", None)
        device_id = request.headers.get("device-id", None)
        app_version = request.headers.get("app-version", None)
        fcm_token = request.data.get("fcm_token", None)

        try:
            if name:
                account.name = name
            if phone_number:
                account.phone_number = phone_number
                account.state = enums.AccountState.ACTIVE
            if password:
                account.password = secure.encrypte_data(password)
            if gender:
                account.gender = gender
            if birth_date:
                account.birth_date = birth_date
            if os:
                account.os = os
            if device_id:
                account.device_id = device_id
            if app_version:
                account.app_version = app_version
            if fcm_token:
                account.fcm_token = fcm_token

            account.save(
                update_fields=[
                    "name",
                    "phone_number",
                    "password",
                    "gender",
                    "birth_date",
                    "os",
                    "device_id",
                    "app_version",
                    "fcm_token",
                    "state",
                ]
            )

            return response.JoodaResponse.success_response()
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)
