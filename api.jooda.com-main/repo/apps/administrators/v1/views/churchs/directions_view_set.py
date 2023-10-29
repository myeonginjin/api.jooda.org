from django.utils.decorators import method_decorator

from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.decorators import action

from common import response, decorators
from apps.churchs.models import ChurchDirections


class ChurchDirectionsViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet
):
    http_method_names = ["post", "patch"]

    @method_decorator(decorators.administrator_authorization())
    def create(self, request):
        administrator = request.administrator
        parking = request.data.get("parking", None)
        own_car = request.data.get("own_car", None)
        public_transport = request.data.get("public_transport", None)
        shuttle_bus = request.data.get("shuttle_bus", None)

        try:
            if ChurchDirections.objects.filter(church=administrator.church).exists():
                return response.JoodaResponse.warning_response(request)

            ChurchDirections.objects.create(
                church=administrator.church,
                parking=parking,
                own_car=own_car,
                public_transport=public_transport,
                shuttle_bus=shuttle_bus,
            )
            return response.JoodaResponse.success_response()
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)

    @method_decorator(decorators.administrator_authorization())
    def patch(self, request):
        administrator = request.administrator
        parking = request.data.get("parking", None)
        own_car = request.data.get("own_car", None)
        public_transport = request.data.get("public_transport", None)
        shuttle_bus = request.data.get("shuttle_bus", None)

        try:
            if not ChurchDirections.objects.filter(
                church=administrator.church
            ).exists():
                ChurchDirections.objects.create(
                    church=administrator.church,
                    parking=parking,
                    own_car=own_car,
                    public_transport=public_transport,
                    shuttle_bus=shuttle_bus,
                )
                return response.JoodaResponse.success_response()

            church_directions = administrator.church.churchdirections
            if parking is not None:
                church_directions.parking = parking
            if own_car is not None:
                church_directions.own_car = own_car
            if public_transport is not None:
                church_directions.public_transport = public_transport
            if shuttle_bus is not None:
                church_directions.shuttle_bus = shuttle_bus

            church_directions.save(
                update_fields=[
                    "parking",
                    "own_car",
                    "public_transport",
                    "shuttle_bus",
                ]
            )
            return response.JoodaResponse.success_response()
        except Exception as e:
            return response.JoodaResponse.error_response(request, error=e)
