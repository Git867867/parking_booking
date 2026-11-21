from django.db import migrations


def migrate_booking_statuses(apps, schema_editor):
    Booking = apps.get_model("bookings", "Booking")
    Booking.objects.filter(is_cancelled=True).update(status="cancelled")
    Booking.objects.filter(is_cancelled=False).update(status="active")


def reverse_booking_statuses(apps, schema_editor):
    Booking = apps.get_model("bookings", "Booking")
    Booking.objects.filter(status="cancelled").update(is_cancelled=True)
    Booking.objects.exclude(status="cancelled").update(is_cancelled=False)


class Migration(migrations.Migration):

    dependencies = [("bookings", "0002_booking_status")]

    operations = [migrations.RunPython(migrate_booking_statuses, reverse_booking_statuses)]