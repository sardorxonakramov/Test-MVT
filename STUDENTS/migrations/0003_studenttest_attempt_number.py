# Generated by Django 5.2.4 on 2025-07-28 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('STUDENTS', '0002_alter_studentanswer_student_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='studenttest',
            name='attempt_number',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
