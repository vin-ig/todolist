# Generated by Django 3.2.9 on 2022-10-20 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goal',
            options={'verbose_name': 'Цель', 'verbose_name_plural': 'Цели'},
        ),
        migrations.AlterModelOptions(
            name='goalcomment',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
    ]
