from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("spots", "0002_alter_spot_daily_rate")]

    operations = [
        migrations.AddField(
            model_name="spot",
            name="is_expensive",
            field=models.GeneratedField(
                db_persist=True,
                expression=models.Case(
                    models.When(daily_rate__gte=500, then=models.Value(True)),
                    default=models.Value(False),
                    output_field=models.BooleanField(),
                ),
                output_field=models.BooleanField(),
                verbose_name="Дорогое место",
            ),
        ),
    ]