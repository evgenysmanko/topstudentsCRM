# Generated by Django 2.1.7 on 2019-04-24 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20190402_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='spisoksm',
            name='departament',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
