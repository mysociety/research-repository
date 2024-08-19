from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource

from repository import models


def construct_model_resource(passed_model):
    class LocalResource(ModelResource):
        class Meta:
            model = passed_model

    return LocalResource


def io_admin_register(passed_model):
    """
    filter that registers ImportExportModelAdmin and
    assigns them a blank model_resource
    """
    model_resource = construct_model_resource(passed_model)

    def inner(admin_cls):
        class ModelAdmin(admin_cls):
            resource_class = model_resource

        admin.site.register(passed_model, ModelAdmin)
        return ModelAdmin

    return inner


@io_admin_register(models.Person)
class PersonAdmin(ImportExportModelAdmin):
    list_display = ("full_name", "institution")
    prepopulated_fields = {"slug": ("first_name", "last_name")}


class ItemAuthorInline(admin.TabularInline):
    model = models.ItemAuthor
    extra = 1


class ResearchOutputInline(admin.TabularInline):
    model = models.ResearchOutput


def migrate_licence(self, request, queryset):
    for model in queryset:
        model.migrate_licence()


migrate_licence.short_description = "Migrate licence"


def create_search_items(self, request, queryset):
    for model in queryset:
        model.create_search_items()


create_search_items.short_description = "Create search items"


@io_admin_register(models.ResearchItem)
class ResearchItemAdmin(ImportExportModelAdmin):
    list_display = (
        "title",
        "friendly_date",
        "author_list",
        "published",
    )
    prepopulated_fields = {"slug": ("title",)}
    inlines = (ItemAuthorInline, ResearchOutputInline)
    filter_horizontal = ("tags",)
    list_filter = ("tags", "published", "featured")
    actions = [migrate_licence, create_search_items]

    def save_model(self, request, obj, form, change):
        # if value of generate thumbnail has changed
        # update

        obj.fetch_toc(save=False)
        super(ImportExportModelAdmin, self).save_model(request, obj, form, change)
        if obj.generate_thumbnail and not obj.thumbnail:
            obj.generate_thumbnail_from_hero()
            obj.save()
        if "zip_archive" in form.changed_data:
            obj.unpack_archive()
        obj.create_search_items()


@io_admin_register(models.Tag)
class TagItemAdmin(ImportExportModelAdmin):
    def save_model(self, request, obj, form, change):
        # if value of generate thumbnail has changed
        # update
        super(ImportExportModelAdmin, self).save_model(request, obj, form, change)
        if obj.generate_thumbnail and not obj.thumbnail:
            obj.generate_thumbnail_from_hero()
            obj.save()


admin.site.register(models.TagGroup)
admin.site.register(models.Site)
admin.site.register(models.ResearchLicence)
admin.site.register(models.SearchItem)
