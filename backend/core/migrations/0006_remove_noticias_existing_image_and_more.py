# Generated by Django 5.1.4 on 2025-05-09 04:17

import core.storage
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_featurednewsorder_remove_noticias_is_featured'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noticias',
            name='existing_image',
        ),
        migrations.RemoveField(
            model_name='noticias',
            name='imagen',
        ),
        migrations.AddField(
            model_name='noticias',
            name='club_logo',
            field=models.ImageField(blank=True, help_text='Club logo to be displayed at the bottom of the article.', null=True, storage=core.storage.CustomStorage(), upload_to='logos/'),
        ),
        migrations.AddField(
            model_name='noticias',
            name='club_logo_existing_image',
            field=models.FilePathField(blank=True, help_text='Or select an existing club logo from assets.', match='.*\\.(jpg|png|jpeg|svg)$', null=True, path='C:\\Users\\ignac\\Escritorio\\Trabajos\\perfectibles\\frontend\\src\\assets', recursive=True),
        ),
        migrations.AddField(
            model_name='noticias',
            name='main_existing_image',
            field=models.FilePathField(blank=True, help_text='Or select an existing main image from assets.', match='.*\\.(jpg|png|jpeg)$', null=True, path='C:\\Users\\ignac\\Escritorio\\Trabajos\\perfectibles\\frontend\\src\\assets', recursive=True),
        ),
        migrations.AddField(
            model_name='noticias',
            name='main_image',
            field=models.ImageField(blank=True, help_text='Main image for the article. Displayed at the top.', null=True, storage=core.storage.CustomStorage(), upload_to='main_images/'),
        ),
        migrations.AlterField(
            model_name='noticias',
            name='cuerpo',
            field=models.TextField(help_text='Main content of the article. Use placeholders like [MEDIA_1], [MEDIA_2] to insert media elements.'),
        ),
        migrations.CreateModel(
            name='EmbeddedMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_type', models.CharField(choices=[('IMAGE', 'Image'), ('VIDEO', 'Video'), ('CAROUSEL', 'Carousel'), ('NONE', 'None')], default='IMAGE', max_length=10)),
                ('title', models.CharField(blank=True, help_text='Optional title for the media element.', max_length=255, null=True)),
                ('file', models.FileField(blank=True, help_text='Upload an image or video file.', null=True, storage=core.storage.CustomStorage(), upload_to='embedded_media/')),
                ('existing_file', models.FilePathField(blank=True, help_text='Or select an existing file from assets.', match='.*\\.(jpg|png|jpeg|mp4|mov|avi)$', null=True, path='C:\\Users\\ignac\\Escritorio\\Trabajos\\perfectibles\\frontend\\src\\assets', recursive=True)),
                ('embed_url', models.URLField(blank=True, help_text='URL for embedding external media (e.g., YouTube video).', null=True)),
                ('alt_text', models.CharField(blank=True, help_text='Alt text for images (accessibility).', max_length=255, null=True)),
                ('caption', models.TextField(blank=True, help_text='Optional caption for the media.', null=True)),
                ('order_in_article', models.PositiveIntegerField(default=0, help_text='Order in which this media appears in the article body (corresponds to [MEDIA_X] placeholders).')),
                ('noticia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='embedded_media', to='core.noticias')),
            ],
            options={
                'verbose_name': 'Embedded Media',
                'verbose_name_plural': 'Embedded Media',
                'ordering': ['order_in_article'],
            },
        ),
    ]
