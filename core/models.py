# encoding: utf-8

from django.db import models
from django.contrib.auth.models import AbstractUser

from .helpers import users_avatar_upload_path


class User(AbstractUser):
    """
    Модель пользователей, унаследованная от Django User
    """

    phone = models.CharField(verbose_name='Телефон', max_length=32, null=True, blank=True)
    skype = models.CharField(verbose_name='Skype', max_length=50, null=True, blank=True)
    site = models.CharField(verbose_name='Cайт', max_length=50, null=True, blank=True)
    city = models.CharField(verbose_name='Город', max_length=50, null=True, blank=True)
    middle_name = models.CharField(max_length=50, blank=True, verbose_name='Отчество', default='')
    birth_date = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    verify_email_uuid = models.CharField(max_length=50, null=True, blank=True)
    avatar_small = models.ImageField(
        verbose_name='Аватар preview', upload_to=users_avatar_upload_path,
        null=True, blank=True, max_length=500)
    avatar = models.ImageField(
        verbose_name='Аватар', upload_to=users_avatar_upload_path, null=True,
        blank=True, max_length=500)

    # objects = models.Manager.from_queryset(RetryQueryset)()

    class Meta:
        db_table = "users"
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
