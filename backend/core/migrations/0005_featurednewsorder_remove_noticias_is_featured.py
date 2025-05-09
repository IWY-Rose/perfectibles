# Generated by Django 5.1.4 on 2025-05-09 02:09

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_noticias_is_featured'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedNewsOrder',
            fields=[
                ('noticia', models.OneToOneField(help_text='The news article to feature.', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='core.noticias')),
                ('added_datetime', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when this noticia was added to the featured list.')),
                ('custom_order', models.PositiveIntegerField(default=0, help_text='Manual order for featured items (lower numbers appear first).')),
            ],
            options={
                'verbose_name': 'Featured News Item',
                'verbose_name_plural': 'Featured News Items',
                'ordering': ['custom_order', '-added_datetime'],
            },
        ),
        migrations.RemoveField(
            model_name='noticias',
            name='is_featured',
        ),
    ]
