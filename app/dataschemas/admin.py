from django.contrib import admin

from .models import DataColumn, DataSchema


class DataColumnInlineAdmin(admin.TabularInline):
    model = DataColumn
    extra = 0


@admin.register(DataSchema)
class DataSchemaAdmin(admin.ModelAdmin):
    autocomplete_fields = ["user"]
    search_fields = ["title", "user__email"]
    list_display = ["title", "user", "created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]
    list_select_related = ["user"]
    inlines = [DataColumnInlineAdmin]
