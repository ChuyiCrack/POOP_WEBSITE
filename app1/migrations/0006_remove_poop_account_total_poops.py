# Generated by Django 5.0 on 2023-12-10 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_rename_poops_poop_account_total_poops_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poop_account',
            name='total_poops',
        ),
    ]