from django.contrib.auth.models import User
from django.db import models

class Label(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Issue(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, related_name="assigned_issues", null=True, on_delete=models.SET_NULL)
    labels = models.ManyToManyField(Label, blank=True)

class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
