from functools import wraps
from common import response, enums
from apps.administrators.models import Administrator


def administrator_authorization() -> Administrator:
    """
    # 관리자 계정 인증
    """

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            authorization_token = request.headers.get("Authorization", None)

            try:
                administrator = Administrator.objects.get(
                    authorization_token=authorization_token
                )

                request.administrator = administrator
            except Administrator.DoesNotExist:
                return response.JoodaResponse.warning_response(
                    request, enums.ErrorCode.FORBIDDEN
                )
            except Exception as e:
                return response.JoodaResponse.error_response(request, error=e)

            return func(request, *args, **kwargs)

        return wrapper

    return decorator
