from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.models import Permission

from authentication.models import Account


class AccountAdmin(UserAdmin):
    ordering = ("email",)
    list_display = (
        "email",
        "first_name",
        "last_name",
        "date_joined",
        "last_login",
        "is_superuser",
    )
    search_fields = ("email", "first_name", "last_name")
    readonly_fields = ("date_joined", "last_login")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Info", {"fields": ("first_name", "last_name")}),
        ("Personal Info", {"fields": ("phone_number",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "first_name", "last_name")}),
        ("Security", {"fields": ("password1", "password2")}),
        ("Personal Info", {"fields": ("phone_number",)}),
        ("Permissions", {"fields": ("is_active", "is_staff")}),
    )


admin.site.register(Account, AccountAdmin)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass
