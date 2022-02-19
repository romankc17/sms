from django.db import models
from PIL import Image
from django.conf import settings
from django.template.defaultfilters import slugify
import datetime

from .accounts import Account

GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
)

def image_path(instance, filename):
    return "/".join(['teachers',slugify(instance.name), filename])


class Teacher(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10,unique=True)
    joining_date = models.DateField(default=datetime.date.today, blank=True)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to='staffs/images/', 
                        # default=f'{settings.MEDIA_ROOT}/staffs/default/he-teacher.png', 
                        null=True, blank=True
                    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    village = models.CharField(max_length=100)
    ward_no = models.IntegerField()
    tole = models.CharField(max_length=100)
    
    def __init__(self, *args, **kwargs):
        super(Teacher, self).__init__(*args, **kwargs)
        


    def __str__(self):
        return self.name

    def save(self,*args, **kwargs,):
        super(Teacher, self).save(*args, **kwargs)

        # check if the image is added or not
        if self.image:
            # compressing image to the size of 300 * 300
            image_path = self.image.path
            img = Image.open(image_path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(image_path)



