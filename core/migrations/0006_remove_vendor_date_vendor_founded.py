# Generated by Django 5.0.6 on 2024-06-25 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_vendor_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='date',
        ),
        migrations.AddField(
            model_name='vendor',
            name='founded',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
