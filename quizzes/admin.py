from django.contrib import admin
from .models import HairProfile

@admin.register(HairProfile)
class HairProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'curl_type', 'porosity', 'density', 'scalp_type', 'budget', 'created_at')
    list_filter = ('curl_type', 'porosity', 'density', 'scalp_type', 'budget')
    search_fields = ('user__username', 'diagnosis_title')
