from django import forms
from django.contrib import admin, messages
from .models import Noticias

class NoticiasAdminForm(forms.ModelForm):
    class Meta:
        model = Noticias
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        existing_image = cleaned_data.get('existing_image')
        imagen = cleaned_data.get('imagen')

        if not imagen and not existing_image:
            raise forms.ValidationError("You must provide either a new image or select an existing one.")

        # Add validation if manually setting featured (optional but good)
        # if cleaned_data.get('is_featured'):
        #    if Noticias.objects.filter(is_featured=True).exclude(pk=self.instance.pk).exists():
        #        # Optionally prevent saving if trying to manually make multiple featured
        #        # Or let the model's save() method handle it silently
        #        pass
        return cleaned_data

# --- Admin Action ---
@admin.action(description='Select as Featured')
def mark_as_featured(modeladmin, request, queryset):
    if queryset.count() != 1:
        modeladmin.message_user(request, "Please select exactly one noticia to mark as featured.", messages.ERROR)
        return

    # Unfeature all others first (the model's save method also does this, but belt-and-suspenders)
    Noticias.objects.update(is_featured=False)

    # Mark the selected one as featured
    noticia = queryset.first()
    noticia.is_featured = True
    noticia.save()

    modeladmin.message_user(request, f'"{noticia.titulo}" has been marked as the featured noticia.', messages.SUCCESS)
# --- End Admin Action ---

class NoticiasAdmin(admin.ModelAdmin):
    form = NoticiasAdminForm
    list_display = ('titulo', 'datetime', 'is_featured', 'imagen', 'existing_image')
    list_filter = ('is_featured', 'datetime')
    actions = [mark_as_featured]
    #search_fields = ('titulo',)  # Fields to search in the admin UI
    #ordering = ('-datetime',)  # Default ordering by datetime descending

admin.site.register(Noticias, NoticiasAdmin)
