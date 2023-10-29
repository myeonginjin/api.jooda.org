from django.contrib import admin


class AccountAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "phone_number")
    list_display = [
        "id",
        "name",
        "phone_number",
        "password",
        "gender",
        "birth_date",
    ]
    list_display_links = ["id"]
    list_per_page = 15
