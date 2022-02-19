from django.db import models
# import DJANGO_SETTINGS_MODULE
from django.conf import settings
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError

from PIL import Image

from classes.models import Section,Batch, Class

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
            # default=f'{settings.MEDIA_ROOT}/students/default/he-student.png', 
            null=True, blank=True
        )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    village = models.CharField(max_length=100)
    ward_no = models.IntegerField()
    tole = models.CharField(max_length=100)
    roll_no = models.IntegerField()
    
    # Many to many relationships with Section model from classes app
    sections = models.ManyToManyField(Section)

    def __str__(self):
        return self.name

    def save(self,*args, **kwargs,):
        super(Student, self).save(*args, **kwargs)

        # compressing image to the size of 300 * 300
        image_path = self.image.path
        img = Image.open(image_path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(image_path)


    # static method to get only the students from latest batch
    @staticmethod
    def get_latest_batch_students():
        return Student.objects.filter(sections__class_name__batch__year=Batch.get_latest_batch().year)

    
