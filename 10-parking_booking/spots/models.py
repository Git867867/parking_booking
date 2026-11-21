from django.db import models
from django.db.models import Case, Value, When
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


class Spot(models.Model):
    number = models.CharField(max_length=10, verbose_name="Номер места")
    covered = models.BooleanField(default=False, verbose_name="Крытое место")
    daily_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость за день",
        help_text="Укажите стоимость одного дня парковки в рублях.",
    )
    # Значение вычисляет база данных (GeneratedField).
    is_expensive = models.GeneratedField(
        expression=Case(
            When(daily_rate__gte=500, then=Value(True)),
            default=Value(False),
            output_field=models.BooleanField(),
        ),
        output_field=models.BooleanField(),
        db_persist=True,
        verbose_name="Дорогое место",
    )
    slug = models.SlugField(max_length=180, unique=True, editable=False, verbose_name="URL-идентификатор")

    def is_suitable_rate(self, max_rate):
        return self.daily_rate <= max_rate

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(f"Место {self.number}")) or "spot"
            if self.pk:
                self.slug = f"{base_slug}-{self.pk}"
            else:
                super().save(*args, **kwargs)
                self.slug = f"{base_slug}-{self.pk}"
                super().save(update_fields=["slug"])
                return
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("spots:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"Место {self.number}"

    class Meta:
        ordering = ["number"]
        verbose_name = "Парковочное место"
        verbose_name_plural = "Парковочные места"