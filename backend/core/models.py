from django.db import models
from .storage import CustomStorage
import os
import logging

logger = logging.getLogger(__name__)

class Noticias(models.Model):
    titulo = models.CharField(max_length=200)
    bajada = models.TextField()
    cuerpo = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='', storage=CustomStorage(), blank=True, null=True)
    existing_image = models.FilePathField(
        path=os.path.join('C:\\Users\\ignac\\Escritorio\\Trabajos\\perfectibles\\frontend\\src\\assets'),  # Update this to your storage directory
        match='.*\.(jpg|png|jpeg)$',
        recursive=False,
        blank=True,
        null=True,
    )
    is_featured = models.BooleanField(default=False, help_text="Mark this noticia as the featured one (only one can be featured).")

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        logger.info(f'Attempting to save noticia: {self.titulo}')
        try:
            # Ensure only one item is featured
            if self.is_featured:
                # Unset is_featured for all other instances
                Noticias.objects.filter(is_featured=True).exclude(pk=self.pk).update(is_featured=False)

            if self.existing_image and not self.imagen:
                # If an existing image is selected, set the imagen field to the existing image's name
                self.imagen.name = os.path.basename(self.existing_image)
            super().save(*args, **kwargs)
            logger.info('Noticia saved successfully.')
        except Exception as e:
            logger.error(f'Error saving noticia: {e}')
