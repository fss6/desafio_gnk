from django.contrib import admin
from django import forms
from .models import Gene, ImportCSV
import csv
from io import StringIO
from celery import shared_task
from celery import Celery
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desafio_gnk.settings')

app = Celery('desafio_gnk')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


class GeneAdmin(admin.ModelAdmin):
  def has_add_permission(self, request):
    return False

  def has_change_permission(self, request, obj=None):
    return False

  def has_delete_permission(self, request, obj=None):
    obj_id = obj.id if not obj is None else 0
    return False if Gene.objects.raw(
        ("SELECT gene.* FROM genes_gene AS gene "
         "INNER JOIN panels_version_genes version ON version.gene_id = gene.id "
         "WHERE gene.id=" + str(obj_id) + "")) else True

class CsvImportForm(forms.Form):
  csv_file = forms.FileField()

class ImportCSVAdmin(admin.ModelAdmin):
  change_list_template = "csv/import_form.html"

  def has_add_permission(self, request):
    return False

  def has_change_permission(self, request, obj=None):
    return False

  @app.task(bind=True)
  def add_genes(self, data):
    for row in data:
      name = row[0]
      if not Gene.objects.filter(name=name).exists():
        gene = Gene(name=name)
        gene.save()

  def changelist_view(self, request, extra_context=None):
    extra_context = extra_context or {}
    if request.method == "POST" and request.FILES.get('csv_file', False):
      csv_file = request.FILES["csv_file"]
      csvf = StringIO(csv_file.read().decode())
      data = csv.reader(csvf, delimiter=',')
      self.add_genes.delay(list(data))
      self.message_user(
          request, "Your csv file is being processed in background")

    return super(ImportCSVAdmin, self).changelist_view(
      request, extra_context=extra_context
    )


admin.site.register(Gene, GeneAdmin)
admin.site.register(ImportCSV, ImportCSVAdmin)
