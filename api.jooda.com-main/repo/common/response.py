from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

from common import enums, slack
from django.conf import settings

from re import split

import logging

logger = logging.getLogger("api")

error_code_to_message = {
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    402: "DUPLICATED_KEY",
    403: "FORBIDDEN",
    405: "PERMISSION_DENIED",
    406: "BAD_PARAMETER_RECEIVED",
    500: "INTERNER_SERVER_ERROR",
}


def unexpected_exception_handler(exc, context):
    """
    # DRF 커스텀 예외 핸들러
    """
    response = exception_handler(exc, context)

    if response is not None:
        del response.data["detail"]
        response.data["success"] = False
        response.data["error"] = {"code": 500, "message": "unexpected error occurred"}

    return response


class JoodaResponse:
    """
    # 주다 표준 응답
    - 성공 : success_response
    - 경고 : warning_response
    - 에러 : error_response
    """

    @staticmethod
    def success_response(data="success"):
        return Response({"success": True, "payload": data})

    @staticmethod
    def warning_response(request, status_code=400, **kwargs):
        channel = enums.SlackChannel.WARNING_LOG
        kwargs["warning"] = error_code_to_message[status_code]
        JoodaResponse.failure_response(request, channel, kwargs)

        return Response(
            {
                "success": False,
                "error_code": status_code,
                "error_message": error_code_to_message.get(status_code, None),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def error_response(request, status_code=500, **kwargs):
        channel = enums.SlackChannel.ERROR_LOG
        JoodaResponse.failure_response(request, channel, kwargs)

        return Response(
            {
                "success": False,
                "error_code": status_code,
                "error_message": error_code_to_message.get(status_code, None),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @staticmethod
    def failure_response(request, channel, kwargs):
        message = JoodaResponse.get_api_url_text(request, kwargs)
        if not settings.TEST:
            if channel == enums.SlackChannel.ERROR_LOG:
                logger.error(message)
            else:
                logger.warning(message)
            slack.Slack(channel).slack_post_texts(message)

    @staticmethod
    def get_api_url_text(request, kwargs) -> str:
        def get_api_url() -> str:
            api_url_list = split("/", request.build_absolute_uri())
            remove_set = {"http:", "https:", "", "localhost"}
            api_url_list = [url for url in api_url_list if url not in remove_set]

            def delete_query_parmas(api_url_list) -> str:
                api_url_list = (
                    api_url_list[: len(api_url_list) - 1]
                    if any(
                        is_queryparams.isdigit() for is_queryparams in api_url_list[-1]
                    )
                    else api_url_list
                )
                return api_url_list

            def sum_api_url_list(api_url_list) -> str:
                result = ""
                for api_url in api_url_list:
                    result += api_url + "/"
                return result

            return sum_api_url_list(delete_query_parmas(api_url_list))

        result = f"[주다복음 {request.method}장 {get_api_url()}절] "
        for key, value in kwargs.items():
            result += f", {key}: {value}"

        return result


def custom404(request, exception=None):
    """
    # 경로 404 에러 처리
    """
    return {"success": False, "error": "wrong approach api"}


def custom500(request, exception=None):
    """
    # 예측 못한 서버 에러 처리
    """
    origin_uri = "http://api.jooda.com/api/"
    origin_secure_uri = "https://api.jooda.com/api/"
    admin_secure_uri = "http://admin.jooda.com/admin-jooda/"
    request_uri = request.build_absolute_uri()
    if not (
        request_uri.startswith(origin_uri)
        or request_uri.startswith(origin_secure_uri)
        or request_uri.startswith(admin_secure_uri)
    ):
        return {"success": False, "error": "wrong approach api"}
    return JoodaResponse.error_response(
        request,
        uri=f"{request.build_absolute_uri()}",
        ip=f"{get_request_ip(request)}",
    )


def get_request_ip(request):
    """
    # request ip 추출
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
