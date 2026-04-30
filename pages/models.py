from django.db import models
from django.urls import reverse

from core.models import SEOFieldsMixin, TimeStampedModel


class Page(TimeStampedModel, SEOFieldsMixin):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    intro = models.TextField(blank=True)
    body = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to="pages/", blank=True, null=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Tag(TimeStampedModel):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class BlogPost(TimeStampedModel, SEOFieldsMixin):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    subtitle = models.CharField(max_length=220, blank=True)
    body = models.TextField()
    cover_image = models.ImageField(upload_to="blog/", blank=True, null=True)
    published_at = models.DateField()
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("pages:blog_detail", kwargs={"slug": self.slug})


class WorkItem(TimeStampedModel):
    company = models.CharField(max_length=140)
    role = models.CharField(max_length=140)
    period = models.CharField(max_length=80)
    details = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"{self.role} at {self.company}"


class Project(TimeStampedModel):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class ProjectLink(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="links")
    label = models.CharField(max_length=60)
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.project}: {self.label}"


class BookmarkGroup(TimeStampedModel):
    title = models.CharField(max_length=120)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class Bookmark(TimeStampedModel):
    group = models.ForeignKey(BookmarkGroup, on_delete=models.CASCADE, related_name="bookmarks")
    label = models.CharField(max_length=160)
    url = models.URLField()
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "label"]

    def __str__(self):
        return self.label


class SocialLink(TimeStampedModel):
    label = models.CharField(max_length=80)
    url = models.CharField(max_length=240)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "label"]

    def __str__(self):
        return self.label
