from django.contrib import admin, messages

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "spot", "user", "spot_rate", "start", "end", "status")
    list_display_links = ("id",)
    search_fields = ("spot__number", "user__name")
    list_filter = ("start", "status")
    ordering = ("-start",)
    list_per_page = 20
    readonly_fields = ("id",)
    list_select_related = ("spot", "user")
    date_hierarchy = "start"
    autocomplete_fields = ("spot", "user")
    actions = ("cancel_bookings", "restore_bookings")

    @admin.display(description="Стоимость за день", ordering="spot__daily_rate")
    def spot_rate(self, obj):
        return obj.spot.daily_rate

    @admin.action(description="Отменить выбранные бронирования")
    def cancel_bookings(self, request, queryset):
        count = 0
        for booking in queryset:
            booking.cancel()
            count += 1
        self.message_user(request, f"Отменено бронирований: {count}.", messages.SUCCESS)

    @admin.action(description="Вернуть в активные")
    def restore_bookings(self, request, queryset):
        updated = queryset.update(status=Booking.Status.ACTIVE)
        self.message_user(request, f"Возвращено бронирований: {updated}.", messages.SUCCESS)