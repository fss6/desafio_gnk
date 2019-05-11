from django.conf import settings
from django.db import models
from enum import Enum
from genes.models import Gene

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

  def approved_versions(self):
    return Version.objects.filter(panel_id=self.id, status=StatusChoice.APPROVED.value).count()


class StatusChoice(Enum):
  PENDING = "Pendente"
  PENDING_APPROVED = "Pendente de aprovação"
  APPROVED = "Aprovado"

class Version(models.Model):
  status = models.CharField(max_length=200, default=StatusChoice.PENDING.value)
  panel = models.ForeignKey(Panel, on_delete=models.CASCADE)
  version = models.IntegerField(default=0)
  created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 null=True, blank=True
                                 )
  genes = models.ManyToManyField(Gene)
  created_at = models.DateTimeField(auto_now_add=True)

  def custom_name(self):
    return self.panel.name + " - V" + str(self.version)

  def custom_version(self):
    return self.version if self.version > 0 else "-"
  custom_version.short_description = 'Version'

  def is_pending(self):
    return self.status == StatusChoice.PENDING.value

  def is_pending_approved(self):
    return self.status == StatusChoice.PENDING_APPROVED.value

  def is_owner(self, user):
    return self.created_by_id == user.id


class Comparation(Version):
  class Meta:
    proxy = True
    verbose_name = 'Comparation'
    verbose_name_plural = 'Comparations'

