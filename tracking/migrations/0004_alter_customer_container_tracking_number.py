# Generated by Django 3.2.7 on 2021-09-17 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0003_auto_20210917_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_container',
            name='tracking_number',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
