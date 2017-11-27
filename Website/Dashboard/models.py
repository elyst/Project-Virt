from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(max_length=255, default="John", verbose_name="Voornaam")
    insertion = models.CharField(max_length=255, default="", blank=True, verbose_name="Tussenvoegsel")
    surname = models.CharField(max_length=255, default="Doe", verbose_name="Tussenvoegsel + Achternaam")
    birthdate = models.DateField(default=timezone.now(), verbose_name="Geboortedatum")
    iban = models.CharField(default="ABCD010123456789", max_length=16, verbose_name="IBAN")
    adres = models.CharField(default="SomeStreet, SomeCity", max_length=255, verbose_name="Adres")
    postalcode = models.CharField(default="1234AB", max_length=6, verbose_name="Postcode")
    phonenumber = models.IntegerField(default="0612345678", verbose_name="Telefoonnummer")
    company = models.CharField(default="-", max_length=255, verbose_name="Bedrijf")
    country = models.CharField(default="Nederland", max_length=255, verbose_name="Land")
    profilepic = models.ImageField(upload_to = 'profiles/', default='/profiles/no-profile.png')

    user = models.ForeignKey(User)
    objects = models.Manager()

    def __str__(self):
        return self.name + " " + self.surname