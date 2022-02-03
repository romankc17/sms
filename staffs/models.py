from django.db import models


class Staff(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)
    salary = models.IntegerField(blank=True, null=True)
    joining_date = models.DateField()
    role = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    image = models.ImageField(upload_to='staffs/images/')


class Address(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)

