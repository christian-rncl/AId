# Generated by Django 2.1.5 on 2019-02-17 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_merchant'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='name',
            field=models.CharField(default='123', max_length=255),
            preserve_default=False,
        ),
    ]
