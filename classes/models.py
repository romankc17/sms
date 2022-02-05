from django.core.exceptions import ValidationError
from django.db import models


class Batch(models.Model):
    year = models.IntegerField(unique=True)

    class Meta:
        verbose_name_plural = 'batches'

    def __str__(self):
        return f'Batch-{self.year}'

class Class(models.Model):
    name = models.CharField(max_length=25,)
    batch = models.ForeignKey(
        Batch, 
        on_delete=models.CASCADE, 
        related_name='classes'
    )

    class Meta:
        verbose_name_plural = 'classes'

    # Raise an error if the class name already exists
    def clean(self):
        if Class.objects.filter(name=self.name, batch=self.batch).exists():
            raise ValidationError('Class already exists')

    def save(self, *args, **kwargs):
        # self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Class-{self.name}|{self.batch}'

class Section(models.Model):
    name = models.CharField(max_length=25)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='sections')

    # Raise Validation error if section already exists
    def clean(self):
        if Section.objects.filter(name=self.name, class_name=self.class_name).exists():
            raise ValidationError('Section already exists')

    def save(self, *args, **kwargs):
        # self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Section-{self.name}|{self.class_name}'
