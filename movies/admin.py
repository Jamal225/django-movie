from django.contrib import admin
from django import forms

from .models import Category, Genre, Movie, MovieShorts, Actor, RatingStar, \
    Rating, Reviews

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание',
                                  widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


class ReviewInline(admin.TabularInline):
    """Отзывы на странице фильма"""
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    inlines = [ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    form = MovieAdminForm
    fieldsets = (
        (None, {
            "fields": [("title", "tagline"), ]
        }),
        (None, {
            "fields": ("description", "poster")
        }),
        (None, {
            "fields": [("year", "world_premiere", "country"), ]
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": [("actors", "directors", "genres", "category"), ]
        }),
        (None, {
            "fields": [("budget", "fees_in_usa", "fees_in_world"), ]
        }),
        ("Options", {
            "fields": [("url", "draft"), ]
        }),
    )


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ("name", "age")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("movie", "ip", "star")


admin.site.register(RatingStar)
