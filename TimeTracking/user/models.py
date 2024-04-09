from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveBigIntegerField(null=True, blank=True)
    is_manager = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)

    class Meta:
        db_table = 'user'

     

