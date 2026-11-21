from django.db import models

from spots.models import Spot
from users.models import User


class BookingQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=self.model.Status.ACTIVE)

    def cancelled(self):
        return self.filter(status=self.model.Status.CANCELLED)

    def completed(self):
        return self.filter(status=self.model.Status.COMPLETED)

    def for_date(self, selected_date):
        return self.filter(start__lte=selected_date, end__gte=selected_date)


class BookingManager(models.Manager.from_queryset(BookingQuerySet)):
    pass


class Booking(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Активно"
        CANCELLED = "cancelled", "Отменено"
        COMPLETED = "completed", "Завершено"

    spot = models.ForeignKey(
        Spot, on_delete=models.PROTECT, related_name="bookings", verbose_name="Парковочное место",
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="bookings", verbose_name="Пользователь",
    )
    start = models.DateField(verbose_name="Дата начала")
    end = models.DateField(verbose_name="Дата окончания")
    status = models.CharField(
        max_length=12, choices=Status.choices, default=Status.ACTIVE, verbose_name="Статус бронирования",
    )

    objects = BookingManager()

    def cancel(self):
        self.status = self.Status.CANCELLED
        self.save(update_fields=["status"])

    def __str__(self):
        return f"{self.spot} — {self.start} ({self.user})"

    class Meta:
        ordering = ["start", "pk"]
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"