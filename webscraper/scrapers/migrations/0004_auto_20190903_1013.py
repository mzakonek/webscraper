# Generated by Django 2.2.4 on 2019-09-03 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapers', '0003_pageurl_imgtask_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageurl',
            name='url',
            field=models.URLField(unique=True),
        ),
    ]
