# Generated by Django 3.1.4 on 2020-12-22 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20201221_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pub_date',
            field=models.DateField(auto_now=True),
        ),
    ]