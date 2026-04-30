from apps.cms.models import NavigationItem, SiteSettings


def global_cms(request):
    return {
        "site_settings": SiteSettings.objects.first(),
        "nav_items": NavigationItem.objects.filter(is_active=True).order_by("order", "id"),
    }
