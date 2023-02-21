from django.contrib import admin

from .models import Category, Genre, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "year", "category", "description")
    list_editable = ("name", "year", "description")
    search_fields = ("name", "year", "category", "genre")
    list_filter = ("name", "year", "category", "genre")
    empty_value_display = "-пусто-"


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "slug",
    )


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "slug",
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
