# Generated by Django 5.1.3 on 2025-02-03 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_comment_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blog_img',
            field=models.ImageField(upload_to='blog_images'),
        ),
    ]
