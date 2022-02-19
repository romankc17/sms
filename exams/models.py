from django.db import models

from classes.models import Class

class Exam(models.Model):
    name = models.CharField(max_lenght=100)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_lenght=100)
    pass_mark = models.IntegerField()
    full_mark = models.IntegerField()
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name
    