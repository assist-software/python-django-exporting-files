from django.db import models
from django.utils.translation import ugettext_lazy
from django.core.validators import MinValueValidator, MaxValueValidator


class Town(models.Model):
    name = models.CharField(max_length=50)
    county = models.CharField(max_length=50)

    class Meta:
        ordering = ['county', 'name']

    def __unicode__(self):
        return self.name


class Weather(models.Model):
    town = models.ForeignKey(
        Town,
        related_name=ugettext_lazy('town'))
    date = models.DateField()
    description = models.TextField()
    max_temperature = models.FloatField()
    min_temperature = models.FloatField()
    wind_speed = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name=ugettext_lazy('wind speed'))
    precipitation = models.IntegerField(
        verbose_name=ugettext_lazy('precipitation'))
    precipitation_probability = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=ugettext_lazy('precipitation probability'))
    observations = models.TextField(
        verbose_name=ugettext_lazy('weather observations'))

    class Meta:
        verbose_name_plural = ugettext_lazy('weather')
        unique_together = (('town', 'date'))
        ordering = ['-date', 'town']

    def __unicode__(self):
        dtos = self.date.strftime('%d-%m-%Y')
        return self.town.name + " " + dtos
