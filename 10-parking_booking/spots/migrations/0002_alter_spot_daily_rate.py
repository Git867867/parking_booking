from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("spots", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="spot",
            name="daily_rate",
            field=models.DecimalField(
                decimal_places=2,
                help_text="Укажите стоимость одного дня парковки в рублях.",
                max_digits=10,
                verbose_name="Стоимость за день",
            ),
        ),
    ]