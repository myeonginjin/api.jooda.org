from django.contrib import admin
from apps.administrators.models import Administrator
from apps.administrators.admin import AdministratorAdmin
from apps.accounts.models import Account
from apps.accounts.admin import AccountAdmin
from apps.churchs.models import (
    Church,
    ChurchDenomination,
    ChurchMember,
    ChurchPastor,
    ChurchHistory,
    ChurchNotice,
    ChurchWeekly,
    ChurchCalendar,
    ChurchWorshipSchedule,
)
from apps.churchs.admin import (
    ChurchAdmin,
    ChurchDenominationAdimin,
    ChurchMemberAdimin,
    ChurchPastorAdmin,
    ChurchHistoryAdmin,
    ChurchNoticeAdmin,
    ChurchWeeklyAdmin,
    ChurchCalendarAdmin,
    ChurchWorshipScheduleAdmin,
)


admin_site = admin.site
admin_site.site_title = "교회 생활의 편리함, 주다"
admin_site.site_header = "교회 생활의 편리함, 주다"
admin_site.index_title = "JooDa, 주다 관리자"


admin_site.register(Administrator, AdministratorAdmin)
admin_site.register(Church, ChurchAdmin)
admin_site.register(Account, AccountAdmin)
admin_site.register(ChurchDenomination, ChurchDenominationAdimin)
admin_site.register(ChurchMember, ChurchMemberAdimin)
admin_site.register(ChurchPastor, ChurchPastorAdmin)
admin_site.register(ChurchHistory, ChurchHistoryAdmin)
admin_site.register(ChurchNotice, ChurchNoticeAdmin)
admin_site.register(ChurchWeekly, ChurchWeeklyAdmin)
admin_site.register(ChurchCalendar, ChurchCalendarAdmin)
admin_site.register(ChurchWorshipSchedule, ChurchWorshipScheduleAdmin)
