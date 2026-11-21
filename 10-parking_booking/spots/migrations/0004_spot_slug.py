from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("spots", "0003_spot_is_expensive")]

    operations = [
        migrations.AddField(
            model_name="spot",
            name="slug",
            field=models.SlugField(blank=True, editable=False, max_length=180, verbose_name="URL-идентификатор"),
        ),
    ]