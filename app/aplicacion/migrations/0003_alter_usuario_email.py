# Generated by Django 3.2 on 2021-05-20 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0002_auto_20210513_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]