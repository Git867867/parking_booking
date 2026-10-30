from django.db import models


class Spot(models.Model):
    number = models.CharField(
        max_length=10,
        verbose_name="Номер места",
    )
    covered = models.BooleanField(
        default=False,
        verbose_name="Крытое место",
    )
    daily_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость за день",
    )

    def is_suitable_rate(self, max_rate):
        return self.daily_rate <= max_rate

    def __str__(self):
        return f"Место {self.number}"

    class Meta:
        ordering = ["number"]
        verbose_name = "Парковочное место"
        verbose_name_plural = "Парковочные места"
