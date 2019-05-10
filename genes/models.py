from django.db import models

class Gene(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
      return self.name
