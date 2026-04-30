from django.contrib import admin
from django.db import models

from core.admin_widgets import CKEditorWidget
from .models import HomePage, NavigationItem, Service, SiteSettings


class RichTextAdminMixin:
    formfield_overrides = {
        models.TextField: {"widget": CKEditorWidget},
    }


class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(RichTextAdminMixin, SingletonAdmin):
    fieldsets = (
        ("Brand", {"fields": ("site_name", "tagline", "logo")}),
        ("Contact", {"fields": ("contact_email", "contact_phone", "address")}),
        (
            "SEO Defaults",
            {"fields": ("seo_title", "seo_description", "seo_keywords", "og_image")},
        ),
    )


@admin.register(HomePage)
class HomePageAdmin(RichTextAdminMixin, SingletonAdmin):
    fieldsets = (
        (
            "Hero",
            {
                "fields": (
                    "hero_title",
                    "hero_subtitle",
                    "hero_image",
                    "cta_text",
                    "cta_url",
                )
            },
        ),
        ("About", {"fields": ("about_title", "about_text")}),
        (
            "SEO",
            {"fields": ("seo_title", "seo_description", "seo_keywords", "og_image")},
        ),
    )


@admin.register(Service)
class ServiceAdmin(RichTextAdminMixin, admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "short_description")
    ordering = ("order", "id")


@admin.register(NavigationItem)
class NavigationItemAdmin(admin.ModelAdmin):
    list_display = ("label", "page", "external_url", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("label",)
    ordering = ("order", "id")
