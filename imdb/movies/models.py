from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.PositiveIntegerField(validators=[MinValueValidator(1800)],
        null=True,
        blank=True)
    rating = models.FloatField(null=True, blank=True)
    director = models.CharField(max_length=255,null=True, blank=True)
    cast = models.TextField(null=True, blank=True)
    story = models.TextField(null=True, blank=True)
    genre = models.CharField(max_length=255,null=True,blank=True)

    class Meta:
        unique_together = ('title','year')
        indexes = [models.Index(fields=['genre'])]

    def __str__(self):
        return self.title