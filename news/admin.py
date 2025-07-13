from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Country, NewsProvider, NewsArticle


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'article_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code')
    list_editable = ('is_active',)
    readonly_fields = ('created_at',)

    def article_count(self, obj):
        return obj.articles.filter(is_active=True).count()
    article_count.short_description = 'Active Articles'


@admin.register(NewsProvider)
class NewsProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'website_link', 'logo_preview', 'is_active', 'article_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'website')
    list_editable = ('is_active',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Provider Information', {
            'fields': ('name', 'website', 'logo_url', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def website_link(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.website, obj.name)
    website_link.short_description = 'Website'

    def logo_preview(self, obj):
        if obj.logo_url:
            return format_html('<img src="{}" style="width: 30px; height: 30px; object-fit: cover;" />', obj.logo_url)
        return "No logo"
    logo_preview.short_description = 'Logo'

    def article_count(self, obj):
        return obj.articles.filter(is_active=True).count()
    article_count.short_description = 'Active Articles'


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    # Main list view - showing exactly the columns you requested
    list_display = ('title_display', 'country', 'news_provider', 'image_preview', 'link_display', 'date_posted')
    list_filter = ('country', 'news_provider', 'date_posted', 'is_active')
    search_fields = ('title', 'description')
    date_hierarchy = 'date_posted'
    readonly_fields = ('views', 'created_at', 'updated_at')
    list_per_page = 25
    
    # Simplified form layout for easy news posting
    fieldsets = (
        ('Post News Article', {
            'fields': ('title', 'country', 'news_provider', 'image', 'link', 'date_posted'),
            'description': 'Fill in the required information to post a news article.'
        }),
        ('Additional Options', {
            'fields': ('description', 'is_active'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def title_display(self, obj):
        max_length = 50
        if len(obj.title) > max_length:
            return obj.title[:max_length] + '...'
        return obj.title
    title_display.short_description = 'Title'

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 4px;" />',
                obj.image
            )
        return "No image"
    image_preview.short_description = 'Image'

    def link_display(self, obj):
        if obj.link:
            return format_html(
                '<a href="{}" target="_blank" title="{}">🔗 View Article</a>',
                obj.link,
                obj.link
            )
        return "No link"
    link_display.short_description = 'Link'

    actions = ['activate_articles', 'deactivate_articles', 'reset_views']

    def activate_articles(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} articles activated.')
    activate_articles.short_description = 'Activate selected articles'

    def deactivate_articles(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} articles deactivated.')
    deactivate_articles.short_description = 'Deactivate selected articles'

    def reset_views(self, request, queryset):
        updated = queryset.update(views=0)
        self.message_user(request, f'Views reset for {updated} articles.')
    reset_views.short_description = 'Reset view count for selected articles'

    # Custom form styling
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }


# Customize admin site header and title
admin.site.site_header = "Daily News Flow Admin"
admin.site.site_title = "News Admin"
admin.site.index_title = "Daily News Flow Administration"
