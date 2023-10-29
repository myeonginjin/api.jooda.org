from django.urls import path, include
from django.http import JsonResponse

from rest_framework import routers

from jooda.admin import admin_site
from common import enums, response

from apps.administrators.v1 import views as AdministratorViewSetV1
from apps.accounts.v1 import views as AccountViewSetV1
from apps.churchs.v1 import views as ChurchViewSetV1
from common.api.v1 import views as CommonViewSetV1

handler404 = response.custom404
handler500 = response.custom500


def health_check(request):
    return JsonResponse({"status": "available"})


router_v1 = routers.SimpleRouter()
##### account #####
router_v1.register(
    r"accounts",
    AccountViewSetV1.AccountViewSet,
    basename="accounts",
)


##### administrator #####
router_v1.register(
    r"administrators/accounts",
    AdministratorViewSetV1.AccountsViewSet,
    basename="administrators/accounts",
)
router_v1.register(
    r"administrators/churchs/info",
    AdministratorViewSetV1.ChurchInfoViewSet,
    basename="administrators/churchs/info",
)
router_v1.register(
    r"administrators/churchs/directions",
    AdministratorViewSetV1.ChurchDirectionsViewSet,
    basename="administrators/churchs/directions",
)
router_v1.register(
    r"administrators/churchs/pastor",
    AdministratorViewSetV1.ChurchPastorViewSet,
    basename="administrators/churchs/pastor",
)
router_v1.register(
    r"administrators/churchs/history",
    AdministratorViewSetV1.ChurchHistoryViewSet,
    basename="administrators/churchs/history",
)
router_v1.register(
    r"administrators/churchs/notice",
    AdministratorViewSetV1.ChurchNoticeViewSet,
    basename="administrators/churchs/notice",
)
router_v1.register(
    r"administrators/churchs/weekly",
    AdministratorViewSetV1.ChurchWeeklyViewSet,
    basename="administrators/churchs/weekly",
)
router_v1.register(
    r"administrators/churchs/member",
    AdministratorViewSetV1.ChurchMemberViewSet,
    basename="administrators/churchs/member",
)
router_v1.register(
    r"administrators/churchs/confirm/member",
    AdministratorViewSetV1.ChurchMemberViewSet.ChurchConfirmMemberViewSet,
    basename="administrators/churchs/confirm/member",
)
router_v1.register(
    r"administrators/churchs/calendar",
    AdministratorViewSetV1.ChurchCalendarViewSet,
    basename="administrators/churchs/calendar",
)
router_v1.register(
    r"administrators/churchs/worship_schedule",
    AdministratorViewSetV1.ChurchWorshipScheduleViewSet,
    basename="administrators/churchs/worship_schedule",
)

##### churchs #####
router_v1.register(
    r"churchs",
    ChurchViewSetV1.ChurchViewSet,
    basename="churchs",
)
router_v1.register(
    r"churchs/pastor",
    ChurchViewSetV1.ChurchPastorViewSet,
    basename="churchs/pastor",
)
router_v1.register(
    r"churchs/notice",
    ChurchViewSetV1.ChurchNoticeViewset,
    basename="churchs/notice",
)
router_v1.register(
    r"churchs/history",
    ChurchViewSetV1.ChurchHistoryViewSet,
    basename="churchs/history",
)
router_v1.register(
    r"churchs/weekly",
    ChurchViewSetV1.ChurchWeeklyViewSet,
    basename="churchs/weekly",
)
router_v1.register(
    r"churchs/worship_schedule",
    ChurchViewSetV1.ChurchWorshipScheduleViewSet,
    basename="churchs/worship_schedule",
)
router_v1.register(
    r"churchs/calendar",
    ChurchViewSetV1.ChurchCalendarViewSet,
    basename="churchs/calendar",
)

##### common #####
router_v1.register(
    r"init",
    CommonViewSetV1.InitViewSet,
    basename="init",
)

urlpatterns = [
    # health check
    path("health_check/", health_check, name="health_check"),
    path(enums.ApiUrl.V1, include(router_v1.urls)),
]

urlpatterns += [
    path("admin-jooda/", admin_site.urls),
]
