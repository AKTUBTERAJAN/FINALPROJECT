# Generated by Django 3.2.4 on 2023-09-18 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='pw',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
