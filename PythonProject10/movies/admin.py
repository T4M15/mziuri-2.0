from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Genre, Director, Actor, Festival, Movie, BoxOffice, Role, Review


class RoleInline(admin.TabularInline):
    model = Role
    extra = 1


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 1


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ("name", "birth_year", "created_at")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "birth_year", "created_at")


@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "start_date", "is_international")


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_year", "director", "age_rating", "is_published")
    list_filter = ("age_rating", "is_published", "director", "genres")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["genres"]
    inlines = [RoleInline, ReviewInline]


@admin.register(BoxOffice)
class BoxOfficeAdmin(admin.ModelAdmin):
    list_display = ("movie", "tickets_sold", "gross")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("movie", "author_name", "rating", "created_at")