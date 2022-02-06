from django.core.exceptions import ValidationError
from django.db import models


class Batch(models.Model):
    year = models.IntegerField(unique=True)

    class Meta:
        verbose_name_plural = 'batches'
        ordering = ('year',)

    def __str__(self):
        return f'Batch-{self.year}'

    # static method to return the latest batch
    @staticmethod
    def get_latest_batch():
        return Batch.objects.all().order_by('-year')[0]

class Class(models.Model):
    name = models.CharField(max_length=25,)
    batch = models.ForeignKey(
        Batch, 
        on_delete=models.CASCADE, 
        related_name='classes'
    )

    class Meta:
        verbose_name_plural = 'classes'
        ordering = ['batch', 'name']

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

    # Raise Validation error if section name already exists in the class
    # only if new section is being created
    # not while updating
    def clean(self):
        if not self.pk and Section.objects.filter(name=self.name, class_name=self.class_name).exists():
            raise ValidationError('Section already exists')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Section-{self.name}|{self.class_name}'
