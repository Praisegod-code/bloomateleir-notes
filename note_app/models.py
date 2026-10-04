from django.db import models
from django.conf import settings

TEMPLATE_CHOICES = [("plain", "Plain"), ("quote", "Quote")]
BACKGROUND_CHOICES = [
    ("none", "None"),
    ("sage", "Sage mist"),
    ("rose", "Rose sand"),
    ("dusk", "Dusk"),
    ("ocean", "Ocean"),
    ("sunlit", "Sunlit"),
    ("midnight", "Midnight"),
]

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notes',
        null=True,
        blank=True,
    )
    attachment = models.FileField(upload_to='note_attachments/', blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    template = models.CharField(max_length=10, choices=TEMPLATE_CHOICES, default="plain")
    background = models.CharField(max_length=20, choices=BACKGROUND_CHOICES, default="none")

    def __str__(self):
        return self.title