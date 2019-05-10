from django.conf import settings
from django.db import models

class Panel(models.Model):
  name = models.CharField(max_length=300, unique=True)
  created_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True
  )
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name
