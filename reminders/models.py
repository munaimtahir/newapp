from django.db import models


class Reminder(models.Model):
    """A reminder parsed from free-form text."""

    original_text = models.TextField()
    parsed_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.original_text} @ {self.parsed_time}"

