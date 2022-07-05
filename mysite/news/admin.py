from django.contrib import admin

from .models import New, Category


class NewAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "time_create", "time_update", "photo", "is_published", "cat")
    list_display_links = ("id", "title", )
    list_editable = ("is_published", )
    list_filter = ("id", )
    search_fields = ("id", "title", "content", )
    prepopulated_fields = {"slug": ("title", )}



class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", )
    list_display_links = ("id", "name", )
    prepopulated_fields = {"slug": ("name", )}


admin.site.register(New, NewAdmin)
admin.site.register(Category, CategoryAdmin)