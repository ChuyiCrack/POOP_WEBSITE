# Generated by Django 5.0 on 2023-12-10 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_poops_owner_shit_alter_poop_account_poops'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poop_account',
            old_name='poops',
            new_name='total_poops',
        ),
        migrations.AlterField(
            model_name='poop_account',
            name='profile_img',
            field=models.ImageField(blank=True, default='./images/default.jpg', upload_to='./images'),
        ),
    ]
