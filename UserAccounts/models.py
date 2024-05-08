from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        related_query_name='custom_user_group'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        related_query_name='custom_user_permission'
    )