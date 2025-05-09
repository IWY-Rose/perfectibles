from django.db import models
from .storage import CustomStorage
import os
import logging
from django.utils import timezone
from django.conf import settings

logger = logging.getLogger(__name__)

# Path for existing image selection - ensure this is correct and accessible
ASSETS_PATH = os.path.join(settings.BASE_DIR, 'frontend', 'src', 'assets')

class Noticias(models.Model):
    titulo = models.CharField(max_length=200)
    bajada = models.TextField()
    cuerpo = models.TextField(help_text="Main content of the article. Use placeholders like [MEDIA_1], [MEDIA_2] to insert media elements.")
    datetime = models.DateTimeField(auto_now_add=True)
    
    # Main image for the article
    main_image = models.ImageField(
        upload_to='main_images/',  # Consider a subfolder within your CustomStorage location
        storage=CustomStorage(), 
        blank=True, 
        null=True,
        help_text="Main image for the article. Displayed at the top."
    )
    main_existing_image = models.FilePathField(
        path=ASSETS_PATH,
        match='.*\.(jpg|png|jpeg)$',
        recursive=True, # Allow searching in subdirectories of assets
        blank=True,
        null=True,
        help_text="Or select an existing main image from assets."
    )

    # Club logo
    club_logo = models.ImageField(
        upload_to='logos/', # Consider a subfolder
        storage=CustomStorage(),
        blank=True,
        null=True,
        help_text="Club logo to be displayed at the bottom of the article."
    )
    club_logo_existing_image = models.FilePathField(
        path=ASSETS_PATH,
        match='.*\.(jpg|png|jpeg|svg)$', # Added SVG for logos
        recursive=True,
        blank=True,
        null=True,
        help_text="Or select an existing club logo from assets."
    )

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        logger.info(f'Attempting to save noticia: {self.titulo}')
        try:
            # Handle main image selection
            if self.main_existing_image and not self.main_image:
                self.main_image.name = os.path.relpath(self.main_existing_image, ASSETS_PATH)
            
            # Handle club logo selection
            if self.club_logo_existing_image and not self.club_logo:
                self.club_logo.name = os.path.relpath(self.club_logo_existing_image, ASSETS_PATH)
            
            super().save(*args, **kwargs)
            logger.info('Noticia saved successfully.')
        except Exception as e:
            logger.error(f'Error saving noticia: {e}')

class EmbeddedMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('IMAGE', 'Image'),
        ('VIDEO', 'Video'),
        ('CAROUSEL', 'Carousel'), # How this is rendered will need frontend logic
        ('NONE', 'None'), # To explicitly mark a position without media if needed
    ]

    noticia = models.ForeignKey(Noticias, related_name='embedded_media', on_delete=models.CASCADE)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='IMAGE')
    title = models.CharField(max_length=255, blank=True, null=True, help_text="Optional title for the media element.")
    
    file = models.FileField(
        upload_to='embedded_media/', # Subfolder in CustomStorage
        storage=CustomStorage(),
        blank=True,
        null=True,
        help_text="Upload an image or video file."
    )
    existing_file = models.FilePathField(
        path=ASSETS_PATH,
        match='.*\.(jpg|png|jpeg|mp4|mov|avi)$', # Added video formats
        recursive=True,
        blank=True,
        null=True,
        help_text="Or select an existing file from assets."
    )
    embed_url = models.URLField(blank=True, null=True, help_text="URL for embedding external media (e.g., YouTube video).")
    
    alt_text = models.CharField(max_length=255, blank=True, null=True, help_text="Alt text for images (accessibility).")
    caption = models.TextField(blank=True, null=True, help_text="Optional caption for the media.")
    
    order_in_article = models.PositiveIntegerField(default=0, help_text="Order in which this media appears in the article body (corresponds to [MEDIA_X] placeholders).")

    class Meta:
        ordering = ['order_in_article']
        verbose_name = "Embedded Media"
        verbose_name_plural = "Embedded Media"

    def __str__(self):
        return f"{self.get_media_type_display()} for '{self.noticia.titulo}' (Order: {self.order_in_article})"

    def save(self, *args, **kwargs):
        if self.existing_file and not self.file:
            self.file.name = os.path.relpath(self.existing_file, ASSETS_PATH)
        super().save(*args, **kwargs)

class FeaturedNewsOrder(models.Model):
    noticia = models.OneToOneField(Noticias, on_delete=models.CASCADE, primary_key=True, help_text="The news article to feature.")
    added_datetime = models.DateTimeField(default=timezone.now, help_text="Timestamp when this noticia was added to the featured list.")
    custom_order = models.PositiveIntegerField(default=0, help_text="Manual order for featured items (lower numbers appear first).")

    class Meta:
        ordering = ['custom_order', '-added_datetime']
        verbose_name = "Featured News Item"
        verbose_name_plural = "Featured News Items"

    def __str__(self):
        return f"Featured: {self.noticia.titulo} (Order: {self.custom_order}, Added: {self.added_datetime.strftime('%Y-%m-%d %H:%M')})"
