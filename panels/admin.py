from django.contrib import admin
from .models import Panel, Version, StatusChoice, Comparation
from genes.models import Gene

class PanelAdmin(admin.ModelAdmin):
  exclude = ('created_by',)
  list_display = ('name', 'approved_versions', 'created_by', 'created_at')
  readonly_fields = ["approved_versions", 'created_by', 'created_at']

  def save_model(self, request, obj, form, change):
    if not change:
      obj.created_by = request.user

    super().save_model(request, obj, form, change)

  def has_change_permission(self, request, obj=None):
    return obj.approved_versions() == 0 if not obj is None else True

  def has_delete_permission(self, request, obj=None):
    return obj.approved_versions() == 0 if not obj is None else True


class VersionAdmin(admin.ModelAdmin):
  list_display = ('panel', 'status', 'custom_version',
                  'created_by', 'created_at')
  exclude = ('created_by', 'status', 'version')
  filter_horizontal = ('genes',)
  readonly_fields = ["status", "custom_version", 'created_by', 'created_at']
  change_form_template = "version/change_status_form.html"

  def save_model(self, request, obj, form, change):
    if not change:
      obj.created_by = request.user

    super().save_model(request, obj, form, change)

  def response_change(self, request, obj):
    if "_make-approve" in request.POST:
      current_version = Version.objects.filter(panel_id=obj.panel.id,
                             status=StatusChoice.APPROVED.value).count()
      obj.status = StatusChoice.APPROVED.value
      obj.version = current_version + 1
      obj.save()
    elif "_make-to-approve" in request.POST:
      obj.status = StatusChoice.PENDING_APPROVED.value
      obj.save()
    elif "_make-disapprove" in request.POST:
      obj.status = StatusChoice.PENDING.value
      obj.save()

    return super().response_change(request, obj)

  def change_view(self, request, object_id, form_url='', extra_context=None):
    extra_context = extra_context or {}
    version = Version.objects.get(id=object_id)
    extra_context['is_pending'] = version.is_pending()
    extra_context['is_pending_approved'] = version.is_pending_approved()
    extra_context['is_owner'] = version.is_owner(request.user)

    return super(VersionAdmin, self).change_view(
        request, object_id, form_url, extra_context=extra_context,
    )

  def has_delete_permission(self, request, obj=None):
    return obj.status == StatusChoice.PENDING.value if not obj is None else True

  def has_change_permission(self, request, obj=None):
    return obj.status == StatusChoice.PENDING.value if not obj is None else True


class ComparationAdmin(admin.ModelAdmin):
  change_list_template = "comparation/comparation_form.html"

  def changelist_view(self, request, extra_context=None):
    extra_context = extra_context or {}
    versions = Version.objects.filter(status=StatusChoice.APPROVED.value)
    extra_context['versions'] = versions
    extra_context['compatible_genes'] = []
    if 'panel_version_a' in request.POST and 'panel_version_b' in request.POST:
      extra_context['compatible_genes'] = Gene.objects.raw(
          ("SELECT gene.* FROM genes_gene AS gene "
           "INNER JOIN panels_version_genes tb_a ON tb_a.gene_id = gene.id "
           "INNER JOIN panels_version_genes tb_b ON tb_b.gene_id = tb_a.gene_id "
           "WHERE tb_a.version_id=" + request.POST.get('panel_version_a') + ""
           " AND tb_b.version_id=" + request.POST.get('panel_version_b')))

    return super(ComparationAdmin, self).changelist_view(
      request, extra_context=extra_context
    )

admin.site.register(Panel, PanelAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(Comparation, ComparationAdmin)
