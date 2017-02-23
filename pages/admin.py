from django.contrib import admin
from pages import models

# tweak to taste - simple at the top and more custom below


admin.site.register(models.Page)



# class FooBarAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ["name"]}
#     list_display  = [ 'slug', 'name', ]
#     search_fields = ['name']
#
# admin.site.register( models.FooBar, FooBarAdmin )
