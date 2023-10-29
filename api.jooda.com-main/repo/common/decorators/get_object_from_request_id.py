from functools import wraps
from common import response
from re import sub


def get_object_from_request_id(model: any):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            def get_lower_model_name(model_name):
                def convert_case(match_obj):
                    return "_" + match_obj.group(1).lower()

                return sub(r"([A-Z]+)", convert_case, model_name)[1:]

            lower_model_name = get_lower_model_name(model.__name__)
            lower_model_id = request.data.get(
                f"{lower_model_name}_id",
                request.query_params.get(
                    f"{lower_model_name}_id", kwargs.get("pk", None)
                ),
            )
            try:
                setattr(
                    request,
                    lower_model_name,
                    model.objects.get(id=lower_model_id),
                )

            except model.DoesNotExist:
                return response.JoodaResponse.warning_response(request)
            except Exception as e:
                return response.JoodaResponse.error_response(request, error=e)

            return func(request, *args, **kwargs)

        return wrapper

    return decorator
