from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100, blank=True)  # Optional title
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title or f"Journal on {self.date_posted.strftime('%m.%d.%Y')}"

    # This method tells django how to find the url to any specific instance of a post
    # The reverse function returns the full url as a string
    def get_absolute_url(self):
        return reverse('journal-detail', kwargs={'pk': self.pk})
