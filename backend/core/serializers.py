from rest_framework import serializers
from .models import Noticias, FeaturedNewsOrder, EmbeddedMedia

class EmbeddedMediaSerializer(serializers.ModelSerializer):
    # Make file URL absolute if using a default FileSystemStorage backend,
    # or ensure your CustomStorage provides full URLs if needed by frontend.
    # If CustomStorage saves to frontend/src/assets, the relative path might be enough
    # if your frontend knows how to construct the full path (e.g. http://127.0.0.1:8000/assets/...).
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = EmbeddedMedia
        fields = (
            'id', 
            'media_type', 
            'title', 
            'file',  # This will be the relative path stored by CustomStorage
            'file_url', # A full URL for the file if possible/needed
            'existing_file', 
            'embed_url', 
            'alt_text', 
            'caption', 
            'order_in_article'
        )

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and hasattr(obj.file, 'url'):
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url # Fallback if request is not in context
        return None

class NoticiaSerializer(serializers.ModelSerializer):
    # Nest EmbeddedMediaSerializer
    # This will serialize all EmbeddedMedia objects related to this Noticia
    embedded_media = EmbeddedMediaSerializer(many=True, read_only=True)
    
    # Similar to EmbeddedMediaSerializer, provide full URLs for images if needed
    main_image_url = serializers.SerializerMethodField()
    club_logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Noticias
        fields = (
            'id', 
            'titulo', 
            'bajada', 
            'cuerpo', 
            'datetime', 
            'main_image', # Relative path from CustomStorage
            'main_image_url',
            'main_existing_image', # This is a FilePathField, stores an absolute path
            'club_logo', # Relative path from CustomStorage
            'club_logo_url',
            'club_logo_existing_image', # FilePathField, absolute path
            'embedded_media' # This will be a list of embedded media items
        )
        # Removed 'imagen' and 'existing_image' as they are renamed

    def get_image_url(self, obj, image_field_name):
        request = self.context.get('request')
        image_field = getattr(obj, image_field_name)
        if image_field and hasattr(image_field, 'url'):
            if request:
                return request.build_absolute_uri(image_field.url)
            return image_field.url
        return None

    def get_main_image_url(self, obj):
        return self.get_image_url(obj, 'main_image')

    def get_club_logo_url(self, obj):
        return self.get_image_url(obj, 'club_logo')


class FeaturedNewsOrderSerializer(serializers.ModelSerializer):
    # NoticiaSerializer is already nested here. 
    # It will now automatically include the updated fields and embedded_media.
    noticia = NoticiaSerializer(read_only=True)

    class Meta:
        model = FeaturedNewsOrder
        fields = ('noticia', 'added_datetime', 'custom_order')
