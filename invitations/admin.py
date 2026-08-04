from django.contrib import admin

from .models import AppConfig, Party, RSVP


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "max_tickets",
        "show_restrictions_text",
        "phone_e164",
        "created_at",
    )
    list_filter = ("show_restrictions_text",)
    search_fields = ("display_name", "phone_e164", "code")


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ("party", "response", "tickets_confirmed", "updated_at")
    list_filter = ("response",)
    search_fields = ("party__display_name",)


@admin.register(AppConfig)
class AppConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "RSVP",
            {
                "fields": ("rsvp_deadline",),
            },
        ),
        (
            "Textos para invitados con restricciones",
            {
                "fields": ("restrictions_text",),
            },
        ),
        (
            "Mensajes de confirmación",
            {
                "fields": (
                    "confirm_yes_text",
                    "confirm_partial_text",
                    "confirm_no_text",
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        return not AppConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
