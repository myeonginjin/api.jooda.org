from django.contrib import admin


from apps.churchs.models import ChurchPastor, ChurchDirections


class ChurchPastorInline(admin.TabularInline):
    model = ChurchPastor
    exclude = [
        "id",
    ]
    extra = 0


class ChurchDirectionsInline(admin.TabularInline):
    model = ChurchDirections
    exclude = [
        "id",
    ]
    extra = 0


class ChurchAdmin(admin.ModelAdmin):
    search_fields = ["id", "name"]
    list_display = [
        "id",
        "name",
        "contact_number",
        "denomination",
        "address",
        "bible_edition",
        "is_exposure",
    ]
    list_display_links = ["name", "denomination"]
    ordering = ["-id"]
    list_per_page = 15
    inlines = (ChurchDirectionsInline, ChurchPastorInline)


class ChurchMemberAdimin(admin.ModelAdmin):
    search_fields = ["id", "account", "church"]
    list_display = [
        "id",
        "account",
        "church",
        "state",
    ]
    ordering = ["-id"]
    list_per_page = 15


class ChurchDenominationAdimin(admin.ModelAdmin):
    search_fields = ["id"]
    list_display = [
        "id",
        "name",
    ]
    list_display_links = ["name"]
    ordering = ["-id"]
    list_per_page = 15


class ChurchPastorAdmin(admin.ModelAdmin):
    search_fields = ("church__name", "name", "role")
    list_display = [
        "id",
        "church",
        "name",
        "role",
    ]
    list_display_link = ["church"]
    list_per_page = 15
    ordering = ["order"]


class ChurchDenominationAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = [
        "id",
        "name",
    ]
    list_display_link = ["name"]
    list_per_page = 15


class ChurchHistoryAdmin(admin.ModelAdmin):
    search_fields = ("church__name", "content")
    list_display = [
        "id",
        "church",
        "year",
        "month",
        "day",
    ]
    list_display_link = ["church"]
    list_per_page = 15


class ChurchNoticeAdmin(admin.ModelAdmin):
    search_fields = ("id", "church__name", "writer__name", "title")
    list_display = [
        "id",
        "church",
        "writer",
        "title",
        "created_at",
    ]
    raw_id_fields = ["church", "writer"]
    list_display_link = ["church"]
    ordering = ["-created_at"]
    list_per_page = 15


class ChurchWeeklyAdmin(admin.ModelAdmin):
    search_fields = ("id", "church__name", "title")
    list_display = [
        "id",
        "church",
        "title",
        "year",
        "month",
        "created_at",
    ]
    raw_id_fields = ["church"]
    list_display_link = ["church"]
    ordering = ["-created_at"]
    list_per_page = 15


class ChurchCalendarAdmin(admin.ModelAdmin):
    search_fields = ("id", "church__name", "title")
    list_display = [
        "id",
        "church",
        "title",
        "start_date",
    ]
    raw_id_fields = ["church"]
    list_display_link = ["church"]
    ordering = ["-start_date"]
    list_per_page = 15


class ChurchCalendarAdmin(admin.ModelAdmin):
    search_fields = ("id", "church__name", "title")
    list_display = [
        "id",
        "church",
        "title",
        "start_date",
    ]
    raw_id_fields = ["church"]
    list_display_link = ["church"]
    ordering = ["-start_date"]
    list_per_page = 15


class ChurchWorshipScheduleAdmin(admin.ModelAdmin):
    search_fields = ("id", "church__name", "title")
    list_display = [
        "id",
        "church",
        "title",
    ]
    raw_id_fields = ["church"]
    list_display_link = ["church"]
    list_per_page = 15
