from django.db import models

class Contact(models.Model):
    email = models.EmailField(unique=True)  # Добавил unique=True для избежания дублей
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"