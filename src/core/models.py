"""Models for the core app."""

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """Custom user model.

    Attributes:
        email (str): The email of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        groups (QuerySet): The groups of the user.
        user_permissions (QuerySet): The permissions of the user.
    """


class Todo(models.Model):
    """Todo model.

    Attributes:
        user (User): The user who created the todo.
        title (str): The title of the todo.
        completed (bool): The status of the todo.
        created_at (datetime): The date and time when the todo was created.
        updated_at (datetime): The date and time when the todo was last updated.
        project (Project): The project to which the todo belongs.
        completed_at (datetime): The date and time when the todo was completed.
        deadline (datetime): The deadline for the todo.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(
        "project.Project", on_delete=models.CASCADE, related_name="todos", null=True
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.title)
