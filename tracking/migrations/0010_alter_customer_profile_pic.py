# Generated by Django 3.2.7 on 2021-10-06 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0009_auto_20210925_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(default='/Koala11.bmp/', upload_to=''),
        ),
    ]
