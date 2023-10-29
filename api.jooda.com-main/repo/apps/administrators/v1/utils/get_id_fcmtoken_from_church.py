from django.db.models.functions import Cast
from django.db.models import CharField
from common import enums
from apps.churchs.models import Church, ChurchMember


def get_id_fcmtoken_from_church(church: Church) -> list:
    queryset = (
        ChurchMember.objects.select_related("account", "church")
        .annotate(str_account_id=Cast("account__id", CharField()))
        .filter(
            church=church,
            state=enums.ChurchMemberState.SUCCESS,
        )
        .values_list("account__fcm_token", "str_account_id")
    )
    if queryset.exists():
        return list(zip(*queryset))[0], list(zip(*queryset))[1]
    else:
        return [], []
