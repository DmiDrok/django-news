from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import New, Category


class NewAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "time_create", "time_update", "get_html_photo", "is_published", "cat")
    list_display_links = ("id", "title", )
    list_editable = ("is_published", )
    list_filter = ("id", "time_create", "cat" )
    search_fields = ("id", "title", "content", )
    prepopulated_fields = {"slug": ("title", )}
    fields = ("title", "slug", "content", "photo", "get_html_photo", "is_published", "cat", "time_create", "time_update")
    readonly_fields = ("time_create", "time_update", "get_html_photo")
    save_on_top = True

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = 'Миниатюра'



class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", )
    list_display_links = ("id", "name", )
    prepopulated_fields = {"slug": ("name", )}


admin.site.register(New, NewAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Администрирование сайта'
admin.site.site_header = 'Администрирование'