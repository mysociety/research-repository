from django.contrib import admin
from repository import models
from import_export.admin import ImportExportModelAdmin
from useful_inkleby.useful_django.admin import io_admin_register


@io_admin_register(models.Person)
class PersonAdmin(ImportExportModelAdmin):
    list_display = ('full_name', 'institution')
    prepopulated_fields = {'slug': ('first_name', 'last_name')}


class ItemAuthorInline(admin.TabularInline):
    model = models.ItemAuthor
    extra = 1


class ResearchOutputInline(admin.TabularInline):
    model = models.ResearchOutput


@io_admin_register(models.ResearchItem)
class ResearchItemAdmin(ImportExportModelAdmin):
    list_display = ('title', 'friendly_date', 'author_list', 'published',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = (ItemAuthorInline, ResearchOutputInline)
    filter_horizontal = ('tags',)
    list_filter = ('tags', 'published', 'featured')

    def save_model(self, request, obj, form, change):
        # if value of generate thumbnail has changed
        # update

        obj.fetch_toc(save=False)

        super(ImportExportModelAdmin, self).save_model(
            request, obj, form, change)
        if obj.generate_thumbnail and not obj.thumbnail:
            obj.generate_thumbnail_from_hero()
            obj.save()


class TagDisplayFilterInline(admin.TabularInline):
    model = models.TagDisplayFilter
    fk_name = "parent"
    extra = 3


@io_admin_register(models.Tag)
class TagItemAdmin(ImportExportModelAdmin):
    inlines = (TagDisplayFilterInline,)


admin.site.register(models.TagGroup)
admin.site.register(models.Site)
