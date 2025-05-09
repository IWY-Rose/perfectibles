from django import forms
from django.contrib import admin, messages
from .models import Noticias, FeaturedNewsOrder, EmbeddedMedia

# Inline Admin for EmbeddedMedia
class EmbeddedMediaInline(admin.TabularInline):
    model = EmbeddedMedia
    form = forms.ModelForm
    fields = ('media_type', 'title', 'file', 'existing_file', 'embed_url', 'alt_text', 'caption', 'order_in_article')
    extra = 1
    ordering = ('order_in_article',)

class NoticiasAdminForm(forms.ModelForm):
    class Meta:
        model = Noticias
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        main_existing_image = cleaned_data.get('main_existing_image')
        main_image = cleaned_data.get('main_image')

        if not main_image and not main_existing_image:
            raise forms.ValidationError("You must provide either a new main image or select an existing one.")
        
        club_logo_existing_image = cleaned_data.get('club_logo_existing_image')
        club_logo = cleaned_data.get('club_logo')

        return cleaned_data

@admin.action(description='Add selected to Featured Banner')
def add_to_featured_banner(modeladmin, request, queryset):
    added_count = 0
    for noticia_item in queryset:
        if not FeaturedNewsOrder.objects.filter(noticia=noticia_item).exists():
            FeaturedNewsOrder.objects.create(noticia=noticia_item)
            added_count += 1
        else:
            messages.warning(request, f'"{noticia_item.titulo}" is already in the featured banner.')
    if added_count > 0:
        modeladmin.message_user(request, f'{added_count} noticia(s) added to the featured banner.', messages.SUCCESS)

@admin.action(description='Remove selected from Featured Banner')
def remove_from_featured_banner(modeladmin, request, queryset):
    removed_count = 0
    for noticia_item in queryset:
        featured_entry = FeaturedNewsOrder.objects.filter(noticia=noticia_item).first()
        if featured_entry:
            featured_entry.delete()
            removed_count += 1
        else:
            messages.warning(request, f'"{noticia_item.titulo}" was not found in the featured banner to remove.')
    if removed_count > 0:
        modeladmin.message_user(request, f'{removed_count} item(s) removed from the featured banner.', messages.SUCCESS)

class NoticiasAdmin(admin.ModelAdmin):
    form = NoticiasAdminForm
    list_display = ('titulo', 'datetime', 'main_image', 'main_existing_image', 'club_logo')
    list_filter = ('datetime',)
    actions = [add_to_featured_banner, remove_from_featured_banner]
    ordering = ('-datetime',)
    
    inlines = [EmbeddedMediaInline]

    fieldsets = (
        (None, {
            'fields': ('titulo', 'bajada', 'cuerpo')
        }),
        ('Main Image', {
            'fields': ('main_image', 'main_existing_image'),
        }),
        ('Club Logo', {
            'fields': ('club_logo', 'club_logo_existing_image'),
        }),
        ('Date Information', {
            'fields': ('datetime',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('datetime',)

admin.site.register(Noticias, NoticiasAdmin)

@admin.register(FeaturedNewsOrder)
class FeaturedNewsOrderAdmin(admin.ModelAdmin):
    list_display = ('noticia_titulo', 'added_datetime', 'custom_order')
    list_editable = ('custom_order',)
    ordering = ('custom_order', '-added_datetime')
    
    def noticia_titulo(self, obj):
        return obj.noticia.titulo
    noticia_titulo.short_description = 'Noticia Title'
    noticia_titulo.admin_order_field = 'noticia__titulo'

    # To prevent direct addition here if you want it only through NoticiasAdmin actions
    # def has_add_permission(self, request):
    #     return False
