# Generated by Django 2.1.5 on 2019-02-16 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20190216_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pin',
            field=models.IntegerField(null=True),
        ),
    ]
