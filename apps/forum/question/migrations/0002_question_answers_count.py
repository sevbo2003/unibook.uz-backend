# Generated by Django 4.0.5 on 2022-07-25 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answers_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
