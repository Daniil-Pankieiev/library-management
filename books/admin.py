from django.contrib import admin
from books.models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date", "isbn", "language", "added_by")
    list_filter = ("language", "published_date")
    search_fields = ("title", "author", "isbn", "language")
    ordering = ("title",)


admin.site.register(Book, BookAdmin)
