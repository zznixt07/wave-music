# Generated by Django 3.1.7 on 2021-04-20 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20210420_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover_image',
            field=models.ImageField(default='userbase/default.jpg', upload_to='album_covers/'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='cover_image',
            field=models.ImageField(default='userbase/default.jpg', upload_to='playlist_covers/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='userbase/default.jpg', upload_to='userbase/'),
        ),
        migrations.AlterField(
            model_name='track',
            name='cover_image',
            field=models.ImageField(default='userbase/default.jpg', upload_to='track_covers/'),
        ),
    ]