# Generated by Django 2.1.5 on 2019-02-17 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20190216_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='amount',
            field=models.IntegerField(null=True),
        ),
    ]