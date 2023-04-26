from django.contrib import admin
from django.db.models.functions import Upper, Lower

from .models import Book, Author, Genre, Comment, Instance


class BookInline(admin.TabularInline):
    model = Book
    max_num = 9


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline]
    list_display = ['last', 'first', 'born']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    class Meta:
        ordering = [Lower('name'), ]


@admin.register(Comment)
class BookAdmin(admin.ModelAdmin):
    list_display = ['text', 'user', 'created']


@admin.register(Instance)
class InstanceAdmin(admin.ModelAdmin):
    list_display = ['book', 'status', 'due_back']
