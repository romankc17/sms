# Generated by Django 4.0.1 on 2022-02-19 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_student_roll_no_delete_studentbatchrollnumber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='salary',
        ),
        migrations.AddField(
            model_name='teacher',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
