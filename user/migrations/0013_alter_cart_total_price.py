# Generated by Django 3.2.4 on 2023-09-20 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_auto_20230920_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.IntegerField(null=True),
        ),
    ]
