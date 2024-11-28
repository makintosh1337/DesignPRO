from django.db import models
from django.contrib.auth.models import User

class Categorys(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")

    def __str__(self):
        return self.name

class Request(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    title = models.CharField(max_length=150, verbose_name="Название заявки")
    description = models.TextField(verbose_name="Описание")
    category = models.ForeignKey(Categorys, on_delete=models.CASCADE, verbose_name="Категория")
    room_image = models.ImageField(upload_to='requests/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='new', verbose_name="Статус")

    def __str__(self):
        return self.title
