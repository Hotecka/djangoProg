# Generated by Django 4.2.2 on 2023-06-13 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_alter_book_options_remove_book_summary_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='book',
            name='language',
        ),
        migrations.AlterField(
            model_name='book',
            name='stock',
            field=models.PositiveIntegerField(default=20),
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
    ]
