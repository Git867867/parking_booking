from django.contrib import admin

from bookings.models import Booking

from .models import User


class BookingInline(admin.TabularInline):
    model = Booking
    fields = ("spot", "start", "end", "status")
    extra = 0
    can_delete = False


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone")
    list_display_links = ("name",)
    search_fields = ("name", "phone")
    ordering = ("name",)
    list_per_page = 20
    readonly_fields = ("id",)
    inlines = (BookingInline,)