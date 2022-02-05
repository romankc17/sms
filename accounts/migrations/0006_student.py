# Generated by Django 4.0.1 on 2022-02-04 14:43

import accounts.models.students
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0003_alter_class_batch_alter_section_class_name'),
        ('accounts', '0005_alter_teacher_gender_alter_teacher_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('roll_no', models.IntegerField()),
                ('dob', models.DateField()),
                ('parent_name', models.CharField(max_length=100)),
                ('parent_contact', models.CharField(max_length=10)),
                ('image', models.ImageField(blank=True, default='/home/roman/school/media/students/default/he-student.png', null=True, upload_to=accounts.models.students.image_path)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('address', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.address')),
                ('sections', models.ManyToManyField(to='classes.Section')),
            ],
        ),
    ]
