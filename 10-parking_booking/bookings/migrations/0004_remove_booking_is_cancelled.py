from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("bookings", "0003_migrate_booking_statuses")]

    operations = [migrations.RemoveField(model_name="booking", name="is_cancelled")]