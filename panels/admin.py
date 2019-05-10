from django.contrib import admin
from .models import Panel

class PanelAdmin(admin.ModelAdmin):
  exclude = ('created_by',)

  def save_model(self, request, obj, form, change):
    if not change:
      obj.created_by = request.user

    super().save_model(request, obj, form, change)

admin.site.register(Panel, PanelAdmin)
