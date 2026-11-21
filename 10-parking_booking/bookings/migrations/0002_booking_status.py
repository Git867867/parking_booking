from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("bookings", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="status",
            field=models.CharField(
                choices=[("active", "Активно"), ("cancelled", "Отменено"), ("completed", "Завершено")],
                default="active",
                max_length=12,
                verbose_name="Статус бронирования",
            ),
        ),
    ]