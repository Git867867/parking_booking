from django.db import models


class User(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Имя пользователя",
    )
    phone = models.CharField(
        max_length=30,
        verbose_name="Телефон",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
