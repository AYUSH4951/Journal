from django.db import models
from django.contrib.auth.models import User

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    ai_analysis = models.TextField(default="No analysis")
    mood = models.CharField(max_length=100, blank=True, default="Neutral")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date.strftime('%Y-%m-%d')}"
