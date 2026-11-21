from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("spots", "0005_populate_spot_slugs")]

    operations = [
        migrations.AlterField(
            model_name="spot",
            name="slug",
            field=models.SlugField(editable=False, max_length=180, unique=True, verbose_name="URL-идентификатор"),
        ),
    ]