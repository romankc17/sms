from this import d
from django.db import models

from .teachers import Teacher
from .students import Student

class Address(models.Model):
    village = models.CharField(max_length=100)
    ward_no = models.IntegerField()
    tole = models.CharField(max_length=100)    
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, 
                    related_name="address", blank=True, null=True
                )
    student = models.OneToOneField(Student, on_delete=models.CASCADE, 
                    related_name="address", blank=True, null=True
                )

    def __str__(self):
        return f"{self.village}-{self.ward_no}, {self.tole}"
