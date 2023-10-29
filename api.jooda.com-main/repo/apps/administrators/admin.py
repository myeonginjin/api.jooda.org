from django.contrib import admin


class AdministratorAdmin(admin.ModelAdmin):
    search_fields = ("id", "church__name")
    list_display = [
        "id",
        "church",
    ]
    list_display_link = ["id"]
    ordering = ["id"]
    list_per_page = 15
    raw_id_fields = ["church"]
