from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from apps.core.models import SEOFieldsMixin, TimeStampedModel


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel, SEOFieldsMixin):
    site_name = models.CharField(max_length=120, default="Company Name")
    tagline = models.CharField(max_length=140, blank=True)
    logo = models.ImageField(upload_to="branding/", blank=True, null=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name


class HomePage(SingletonModel, SEOFieldsMixin):
    hero_title = models.CharField(max_length=120, default="Welcome to our company")
    hero_subtitle = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to="home/", blank=True, null=True)
    cta_text = models.CharField(max_length=40, blank=True)
    cta_url = models.CharField(max_length=200, blank=True)

    about_title = models.CharField(max_length=120, blank=True)
    about_text = models.TextField(blank=True)

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Page"

    def __str__(self):
        return "Homepage"


class Service(TimeStampedModel):
    title = models.CharField(max_length=120)
    short_description = models.TextField()
    image = models.ImageField(upload_to="services/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class NavigationItem(TimeStampedModel):
    label = models.CharField(max_length=60)
    page = models.ForeignKey(
        "pages.Page",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="menu_items",
    )
    external_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def clean(self):
        if not self.page and not self.external_url:
            raise ValidationError("Add either an internal page or an external URL.")
        if self.page and self.external_url:
            raise ValidationError("Choose only one: internal page or external URL.")

    def get_url(self):
        if self.external_url:
            return self.external_url
        if self.page:
            return reverse("pages:page_detail", kwargs={"slug": self.page.slug})
        return "#"

    def __str__(self):
        return self.label
