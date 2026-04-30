from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import BlogPost, Page


class StaticViewSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "pages:blog",
            "pages:work",
            "pages:projects",
            "pages:bookmarks",
            "pages:tags",
            "pages:contact",
        ]

    def location(self, item):
        return reverse(item)


class PageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Page.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("pages:page_detail", kwargs={"slug": obj.slug})


class BlogPostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at
