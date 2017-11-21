from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(max_length=255, default="John", verbose_name="Voornaam")
    insertion = models.CharField(max_length=255, default="", blank=True, verbose_name="Tussenvoegsel")
    surname = models.CharField(max_length=255, default="Doe", verbose_name="Tussenvoegsel + Achternaam")
    birthdate = models.DateField(default=timezone.now(), verbose_name="Geboortedatum")
    user = models.ForeignKey(User)

    objects = models.Manager()

    def __str__(self):
        return self.name + " " + self.surname