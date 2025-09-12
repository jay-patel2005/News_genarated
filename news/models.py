from django.db import models

class News(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    url = models.URLField(blank=True, null=True)
    source = models.CharField(max_length=100, default='Unknown')
    category = models.CharField(max_length=50, default='General')
    published_at = models.DateTimeField()

    def __str__(self):
        return self.title

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


from django.contrib.auth.models import User
from django.db import models

class SavedArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.URLField()
    published_at = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} saved {self.title}"
