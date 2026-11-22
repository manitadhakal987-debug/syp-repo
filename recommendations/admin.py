from django.contrib import admin
from .models import CurlCareRule

@admin.register(CurlCareRule)
class CurlCareRuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'rule_type', 'rule_key', 'priority')
    list_filter = ('rule_type', 'priority')
    search_fields = ('title', 'summary', 'ingredients_recommended')
