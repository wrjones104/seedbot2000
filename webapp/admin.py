from django.contrib import admin
from .models import Tag, Preset

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Preset)
class PresetAdmin(admin.ModelAdmin):
    list_display = ('preset_name', 'creator_name', 'official', 'hidden', 'validation_status')
    list_filter = ('official', 'hidden', 'validation_status', 'tags')
    search_fields = ('preset_name', 'creator_name', 'description')
    filter_horizontal = ('tags',)
