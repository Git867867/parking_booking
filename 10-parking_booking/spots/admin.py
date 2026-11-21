from django.contrib import admin
from django.db.models import Count, Q

from bookings.models import Booking

from .models import Spot


class BookingInline(admin.TabularInline):
    model = Booking
    fields = ("user", "start", "end", "status")
    extra = 0
    can_delete = False


@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    list_display = ("id", "number", "covered", "daily_rate", "is_expensive", "active_bookings_count")
    list_display_links = ("number",)
    list_editable = ("daily_rate",)
    search_fields = ("number",)
    list_filter = ("covered",)
    ordering = ("number",)
    list_per_page = 20
    readonly_fields = ("id",)
    inlines = (BookingInline,)
    view_on_site = True

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            active_bookings=Count("bookings", filter=Q(bookings__status=Booking.Status.ACTIVE)),
        )

    @admin.display(description="Активных бронирований", ordering="active_bookings")
    def active_bookings_count(self, obj):
        return obj.active_bookings