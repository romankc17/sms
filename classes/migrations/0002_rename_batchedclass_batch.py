# Generated by Django 4.0.1 on 2022-01-30 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BatchedClass',
            new_name='Batch',
        ),
    ]