from django.db import migrations
from django.utils.text import slugify
from unidecode import unidecode


def populate_spot_slugs(apps, schema_editor):
    Spot = apps.get_model("spots", "Spot")
    for spot in Spot.objects.all().order_by("pk"):
        base_slug = slugify(unidecode(f"Место {spot.number}")) or "spot"
        spot.slug = f"{base_slug}-{spot.pk}"
        spot.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [("spots", "0004_spot_slug")]

    operations = [migrations.RunPython(populate_spot_slugs, migrations.RunPython.noop)]