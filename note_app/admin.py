from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at", "updated_at", "is_deleted")
    list_filter = ("user", "is_deleted", "created_at")
    search_fields = ("title", "content", "user__username")