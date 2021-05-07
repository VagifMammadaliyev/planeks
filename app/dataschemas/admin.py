from django.contrib import admin

from .models import DataColumn, DataSchema, DataSet


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


@admin.register(DataSet)
class DataSetAdmin(admin.ModelAdmin):
    autocomplete_fields = ["schema"]
    search_fields = ["schema__title", "schema__user__email"]
    list_display = [
        "schema",
        "started_generation_at",
        "finished_generation_at",
        "generated_file",
        "is_finished",
    ]
    readonly_fields = [
        "created_at",
        "finished_generation_at",
        "started_generation_at",
        "is_started",
        "is_finished",
        "is_processing",
    ]
    list_select_related = ["schema"]
