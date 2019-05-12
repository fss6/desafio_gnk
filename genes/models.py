from django.db import models

class Gene(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
      return self.name


class ImportCSV(Gene):
  class Meta:
    proxy = True
    verbose_name = 'Import CSV'
    verbose_name_plural = 'Import CSV'
