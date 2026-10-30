from django.db import models

from spots.models import Spot
from users.models import User


class Booking(models.Model):
    spot = models.ForeignKey(
        Spot,
        on_delete=models.PROTECT,
        related_name="bookings",
        verbose_name="Парковочное место",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="bookings",
        verbose_name="Пользователь",
    )
    start = models.DateField(
        verbose_name="Дата начала",
    )
    end = models.DateField(
        verbose_name="Дата окончания",
    )
    is_cancelled = models.BooleanField(
        default=False,
        verbose_name="Бронирование отменено",
    )

    def cancel(self):
        self.is_cancelled = True
        self.save(update_fields=["is_cancelled"])

    def __str__(self):
        return f"{self.spot} — {self.start} ({self.user})"

    class Meta:
        ordering = ["start", "pk"]
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
