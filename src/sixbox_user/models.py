from django.db import models


# Create your models here.

class S_User(models.Model):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    first_name = models.CharField('first name', max_length=100, null=True)
    last_name = models.CharField('last name', max_length=100, null=True)
    image = models.ImageField(blank=True)
    number = models.CharField(max_length=30, unique=True, null=True)


