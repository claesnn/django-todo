from django.db import models


class Project(models.Model):
    class Technology(models.TextChoices):
        PYTHON = "Python"
        DJANGO = "Django"
        JAVASCRIPT = "JavaScript"
        REACT = "React"
        ANGULAR = "Angular"
        FLUTTER = "Flutter"
        HTML = "HTML"
        CSS = "CSS"
        BOOTSTRAP = "Bootstrap"
        MATERIALIZE = "Materialize"
        MYSQL = "MySQL"
        POSTGRESQL = "PostgreSQL"
        MONGODB = "MongoDB"
        FIREBASE = "Firebase"
        HEROKU = "Heroku"

    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(choices=Technology.choices, max_length=50)

    def __str__(self):
        return str(self.title)
