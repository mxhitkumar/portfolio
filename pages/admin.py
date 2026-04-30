from django.contrib import admin
from django.db import models

from core.admin_widgets import CKEditorWidget

from .models import (
    BlogPost,
    Bookmark,
    BookmarkGroup,
    Page,
    Project,
    ProjectLink,
    SocialLink,
    Tag,
    WorkItem,
)


class RichTextAdminMixin:
    formfield_overrides = {
        models.TextField: {"widget": CKEditorWidget},
    }


@admin.register(Page)
class PageAdmin(RichTextAdminMixin, admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title", "slug", "intro", "body")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("Content", {"fields": ("title", "slug", "hero_image", "intro", "body", "is_published")}),
        (
            "SEO",
            {"fields": ("seo_title", "seo_description", "seo_keywords", "og_image")},
        ),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(BlogPost)
class BlogPostAdmin(RichTextAdminMixin, admin.ModelAdmin):
    list_display = ("title", "published_at", "is_published", "is_featured", "updated_at")
    list_filter = ("is_published", "is_featured", "tags", "published_at")
    search_fields = ("title", "subtitle", "body")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    date_hierarchy = "published_at"
    fieldsets = (
        ("Content", {"fields": ("title", "slug", "subtitle", "cover_image", "body")}),
        ("Publishing", {"fields": ("published_at", "tags", "is_published", "is_featured")}),
        ("SEO", {"fields": ("seo_title", "seo_description", "seo_keywords", "og_image")}),
    )


@admin.register(WorkItem)
class WorkItemAdmin(RichTextAdminMixin, admin.ModelAdmin):
    list_display = ("company", "role", "period", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("company", "role", "period", "details")
    ordering = ("order", "-created_at")


class ProjectLinkInline(admin.TabularInline):
    model = ProjectLink
    extra = 1


@admin.register(Project)
class ProjectAdmin(RichTextAdminMixin, admin.ModelAdmin):
    list_display = ("title", "slug", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = (ProjectLinkInline,)
    ordering = ("order", "title")


class BookmarkInline(admin.TabularInline):
    model = Bookmark
    formfield_overrides = {
        models.TextField: {"widget": CKEditorWidget},
    }
    extra = 1


@admin.register(BookmarkGroup)
class BookmarkGroupAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title",)
    inlines = (BookmarkInline,)
    ordering = ("order", "title")


@admin.register(Bookmark)
class BookmarkAdmin(RichTextAdminMixin, admin.ModelAdmin):
    list_display = ("label", "group", "order", "is_active")
    list_filter = ("group", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("label", "description", "url")


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "url", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("label", "url")
