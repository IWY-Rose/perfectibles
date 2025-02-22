from django import forms
from django.contrib import admin
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
        return cleaned_data

class NoticiasAdmin(admin.ModelAdmin):
    form = NoticiasAdminForm
    list_display = ('titulo', 'datetime', 'imagen', 'existing_image')
    #search_fields = ('titulo',)  # Fields to search in the admin UI
    #ordering = ('-datetime',)  # Default ordering by datetime descending

admin.site.register(Noticias, NoticiasAdmin)
