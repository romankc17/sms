from pyexpat import model
from django.db import models


class Class(models.Model):
    name  = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'classes'

    def __str__(self):
        return f'Class-{self.name}'

class Batch(models.Model):
    year = models.IntegerField()
    classes = models.ManyToManyField(Class)

    class Meta:
        verbose_name_plural = 'batches'

    def __str__(self):
        return f'Batch-{self.year}'

class ClassBatch(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    batch_name = models.ForeignKey(Batch, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'class_batches'

    def __str__(self):
        return f'Class-{self.class_name.name} Batch-{self.batch_name.year}'

class Section(models.Model):
    name = models.CharField(max_length=100)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f'Section-{self.name}|{self.class_name}|{self.batch}'
