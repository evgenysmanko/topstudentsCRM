# Generated by Django 2.1.7 on 2019-04-24 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_remove_spisoksm_departament'),
    ]

    operations = [
        migrations.AddField(
            model_name='spisoksm',
            name='departament',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
