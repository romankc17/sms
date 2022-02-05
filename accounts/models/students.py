from django.db import models
# import DJANGO_SETTINGS_MODULE
from django.conf import settings
# import slugify
from django.template.defaultfilters import slugify

from PIL import Image

from classes.models import Section

# function returning custom image path
def image_path(instance, filename):
    return '/'.join(['students', slugify(instance.name), filename])

#gender choices tuple for students
GENDER_CHOICES = (
    ('M',"Male"), 
    ("F","Female")
)

class Student(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()
    parent_name = models.CharField(max_length=100)
    parent_contact = models.CharField(max_length=10)
    image = models.ImageField(
            upload_to=image_path, 
            default=f'{settings.MEDIA_ROOT}/students/default/he-student.png', 
            null=True, blank=True
        )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    # Many to many relationships with Section model from classes app
    sections = models.ManyToManyField(Section)


    def save(self,*args, **kwargs,):
        super(Student, self).save(*args, **kwargs)

        # compressing image to the size of 300 * 300
        image_path = self.image.path
        img = Image.open(image_path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(image_path)


# Model to keep record of students' roll_no at different batch
class StudentRollNo(models.Model):
    roll_no = models.IntegerField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)


    
