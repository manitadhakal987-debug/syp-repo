from django.contrib import admin
from .models import Category, SuitabilityTag, Product, HaircutGuide

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon_name')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SuitabilityTag)
class SuitabilityTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'badge_color')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'stock', 'is_available', 'is_featured')
    list_editable = ('price', 'stock', 'is_available', 'is_featured')
    list_filter = ('category', 'is_available', 'is_featured', 'brand')
    search_fields = ('name', 'brand', 'ingredients_list', 'key_actives')
    prepopulated_fields = {'slug': ('brand', 'name')}
    filter_horizontal = ('suitability_tags',)

@admin.register(HaircutGuide)
class HaircutGuideAdmin(admin.ModelAdmin):
    list_display = ('name', 'suitable_curls', 'face_shapes')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description', 'nepal_salon_advice')
