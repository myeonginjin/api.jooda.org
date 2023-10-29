from functools import wraps
from common import response, slack, enums
from apps.accounts.models import Account
from django.conf import settings
from django.core.exceptions import ValidationError


def account_autorization() -> Account:
    """
    # 회원 계정 인증
    """

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            account_id = request.headers.get("Authorization", None)
            os = request.headers.get("os", None)
            device_id = request.headers.get("device-id", None)
            app_version = request.headers.get("app-version", None)

            try:
                account = Account.objects.get(id=account_id)
                account.os = os
                account.device_id = f"{os}-{device_id}"

                account.save(update_fields=["os", "device_id"])

                request.account = account

            except Account.DoesNotExist:
                return response.JoodaResponse.warning_response(
                    request, enums.ErrorCode.FORBIDDEN
                )

            except ValidationError:
                if settings.JOODA_GUEST_AUTHORIZATION == account_id:
                    request.account = None
                    return func(request, *args, **kwargs)
                return response.JoodaResponse.warning_response(
                    request, enums.ErrorCode.PERMISSION_DENIED
                )

            except Exception as e:
                return response.JoodaResponse.error_response(request, error=e)

            return func(request, *args, **kwargs)

        return wrapper

    return decorator
