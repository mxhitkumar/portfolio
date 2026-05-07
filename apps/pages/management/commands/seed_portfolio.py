from datetime import date

from django.core.management.base import BaseCommand

from apps.cms.models import HomePage, NavigationItem, Service, SiteSettings
from apps.pages.models import (
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


class Command(BaseCommand):
    help = "Seed the portfolio with polished starter content."

    def handle(self, *args, **options):
        self.seed_site_settings()
        self.seed_home_page()
        pages = self.seed_pages()
        tags = self.seed_tags()
        self.seed_services()
        self.seed_work_items()
        self.seed_projects()
        self.seed_blog_posts(tags)
        self.seed_bookmarks()
        self.seed_social_links()
        self.seed_navigation(pages)
        self.stdout.write(self.style.SUCCESS("Portfolio seed content is ready."))

    def seed_site_settings(self):
        settings = SiteSettings.load()
        if settings.site_name in {"", "Company Name"}:
            settings.site_name = "Mohit Kumar"
        if not settings.tagline:
            settings.tagline = "Django developer building fast, useful, production-ready web apps."
        if not settings.contact_email:
            settings.contact_email = "hello@example.com"
        if not settings.seo_title:
            settings.seo_title = "Mohit Kumar | Django Portfolio"
        if not settings.seo_description:
            settings.seo_description = (
                "Portfolio of a Django developer focused on reliable backends, clean "
                "interfaces, deployment, and practical product thinking."
            )
        if not settings.seo_keywords:
            settings.seo_keywords = "Django, Python, portfolio, web developer, Render"
        settings.save()

    def seed_home_page(self):
        home = HomePage.load()
        if home.hero_title in {"", "Welcome to our company"}:
            home.hero_title = "Django developer with production instincts"
        if not home.hero_subtitle:
            home.hero_subtitle = (
                "I build clean Django applications, thoughtful admin workflows, and "
                "deployable systems that stay simple under pressure."
            )
        if not home.cta_text:
            home.cta_text = "See projects"
        if not home.cta_url:
            home.cta_url = "/projects/"
        if not home.about_title:
            home.about_title = "About this portfolio"
        if not home.about_text:
            home.about_text = (
                "This site highlights three years of focused growth across Python, Django, "
                "SQLite, deployment, content systems, and user-facing product details."
            )
        if not home.seo_title:
            home.seo_title = "Mohit Kumar | Django Developer"
        if not home.seo_description:
            home.seo_description = (
                "A practical Django portfolio with projects, writing, work notes, and "
                "production deployment details."
            )
        home.save()

    def seed_pages(self):
        pages = {}
        page_data = [
            {
                "title": "About",
                "slug": "about",
                "intro": "A short story of the last three years of building for the web.",
                "body": (
                    "<p>I am a Django developer who enjoys turning rough ideas into useful "
                    "software. Over the last three years I have worked through the full path "
                    "of building web projects: data modeling, forms, admin customization, "
                    "templates, deployment, static files, and maintainable settings.</p>"
                    "<p>My current focus is simple production-ready systems: clear database "
                    "models, readable views, stable deployment, good content structure, and "
                    "interfaces people can understand quickly.</p>"
                ),
                "seo_title": "About Mohit Kumar",
                "seo_description": "About a Django developer focused on practical, production-ready web apps.",
            },
            {
                "title": "Now",
                "slug": "now",
                "intro": "What I am practicing and improving right now.",
                "body": (
                    "<p>I am sharpening my Django fundamentals, deployment workflow, and "
                    "ability to explain technical decisions clearly. I care about small "
                    "details because they make projects easier to trust.</p>"
                    "<p>Recent focus areas include Render deployment, SQLite persistence, "
                    "WhiteNoise static files, SEO metadata, reusable templates, and seed data "
                    "for clean first launches.</p>"
                ),
                "seo_title": "Now | Mohit Kumar",
                "seo_description": "Current focus areas across Django, deployment, and product-ready web development.",
            },
        ]
        for data in page_data:
            page, _ = Page.objects.get_or_create(
                slug=data["slug"],
                defaults={**data, "is_published": True},
            )
            pages[data["slug"]] = page
        return pages

    def seed_tags(self):
        tags = {}
        for name, slug in [
            ("Django", "django"),
            ("Python", "python"),
            ("Deployment", "deployment"),
            ("Product Thinking", "product-thinking"),
            ("Learning", "learning"),
        ]:
            tag, _ = Tag.objects.get_or_create(slug=slug, defaults={"name": name})
            tags[slug] = tag
        return tags

    def seed_services(self):
        services = [
            (
                "Django Web Applications",
                "Clean models, views, templates, forms, admin workflows, and deployment-ready settings.",
            ),
            (
                "Portfolio and CMS Setup",
                "Editable pages, blog posts, navigation, SEO fields, and content structure that can grow.",
            ),
            (
                "Render Deployment",
                "Production settings, Gunicorn, WhiteNoise, persistent SQLite storage, and deployment checks.",
            ),
        ]
        for order, (title, description) in enumerate(services, start=1):
            Service.objects.get_or_create(
                title=title,
                defaults={
                    "short_description": description,
                    "order": order,
                    "is_active": True,
                },
            )

    def seed_work_items(self):
        items = [
            {
                "company": "Independent Practice",
                "role": "Django Developer",
                "period": "2024 - Present",
                "details": (
                    "<p>Built and refined Django portfolio systems with CMS-style content, "
                    "blog publishing, contact submissions, SEO fields, and production deployment.</p>"
                ),
                "order": 1,
            },
            {
                "company": "Project Lab",
                "role": "Python and Web Development Learner",
                "period": "2023 - 2024",
                "details": (
                    "<p>Practiced Python fundamentals, database modeling, templates, routing, "
                    "admin customization, and reusable app structure.</p>"
                ),
                "order": 2,
            },
            {
                "company": "Foundation Year",
                "role": "Frontend and Backend Explorer",
                "period": "2022 - 2023",
                "details": (
                    "<p>Learned how web pages, forms, static files, content, and deployment "
                    "fit together into complete user-facing projects.</p>"
                ),
                "order": 3,
            },
        ]
        for data in items:
            WorkItem.objects.get_or_create(
                company=data["company"],
                role=data["role"],
                defaults={**data, "is_active": True},
            )

    def seed_projects(self):
        projects = [
            {
                "title": "Production Portfolio CMS",
                "slug": "production-portfolio-cms",
                "description": (
                    "<p>A Django portfolio with editable site settings, pages, blog posts, "
                    "projects, bookmarks, contact submissions, SEO metadata, and Render deployment.</p>"
                    "<p><strong>Highlights:</strong> clean app structure, admin-first content "
                    "management, reusable templates, WhiteNoise static files, and SQLite persistence.</p>"
                ),
                "order": 1,
                "links": [("Source", "https://github.com/")],
            },
            {
                "title": "Deployment-Ready Django Starter",
                "slug": "deployment-ready-django-starter",
                "description": (
                    "<p>A focused setup for taking a Django project from local development to "
                    "production with environment variables, secure settings, migrations, and static files.</p>"
                ),
                "order": 2,
                "links": [("Notes", "/blog/render-deployment-checklist/")],
            },
            {
                "title": "Knowledge Library",
                "slug": "knowledge-library",
                "description": (
                    "<p>A curated bookmark and writing system for tracking useful engineering "
                    "resources, decisions, and reusable learning notes.</p>"
                ),
                "order": 3,
                "links": [("Bookmarks", "/bookmarks/")],
            },
        ]
        for data in projects:
            links = data.pop("links")
            project, _ = Project.objects.get_or_create(
                slug=data["slug"],
                defaults={**data, "is_active": True},
            )
            for order, (label, url) in enumerate(links, start=1):
                ProjectLink.objects.get_or_create(
                    project=project,
                    label=label,
                    defaults={"url": url, "order": order},
                )

    def seed_blog_posts(self, tags):
        posts = [
            {
                "title": "Render Deployment Checklist for Django",
                "slug": "render-deployment-checklist",
                "subtitle": "The small production details that make a Django app feel finished.",
                "published_at": date(2026, 5, 1),
                "body": (
                    "<p>A reliable deployment needs more than a working homepage. I check "
                    "environment variables, static file collection, migrations, allowed hosts, "
                    "CSRF origins, secure cookies, and a repeatable startup command.</p>"
                    "<p>For this portfolio, the production setup uses Gunicorn, WhiteNoise, "
                    "Render environment variables, and SQLite on a persistent disk.</p>"
                ),
                "tag_slugs": ["django", "deployment"],
                "is_featured": True,
            },
            {
                "title": "What Three Years of Web Learning Taught Me",
                "slug": "three-years-of-web-learning",
                "subtitle": "Consistency beats shortcuts when building real projects.",
                "published_at": date(2025, 11, 18),
                "body": (
                    "<p>The biggest improvement came from building complete things: models, "
                    "views, templates, forms, admin screens, static files, and deployment. "
                    "Every finished project made the next one easier to reason about.</p>"
                    "<p>I learned that impressive work is usually clear work: simple structure, "
                    "good naming, good defaults, and enough polish that someone can use it immediately.</p>"
                ),
                "tag_slugs": ["learning", "product-thinking"],
                "is_featured": True,
            },
            {
                "title": "Why I Like Django for Portfolio Projects",
                "slug": "why-django-for-portfolio-projects",
                "subtitle": "Django gives small projects a serious backbone.",
                "published_at": date(2025, 3, 12),
                "body": (
                    "<p>Django is a strong fit for portfolio projects because it includes the "
                    "parts most sites eventually need: authentication, admin, forms, routing, "
                    "templates, migrations, and a clear project structure.</p>"
                    "<p>That lets me spend more time on content, user experience, and deployment "
                    "instead of rebuilding the same foundation again and again.</p>"
                ),
                "tag_slugs": ["django", "python"],
                "is_featured": False,
            },
        ]
        for data in posts:
            tag_slugs = data.pop("tag_slugs")
            post, _ = BlogPost.objects.get_or_create(
                slug=data["slug"],
                defaults={
                    **data,
                    "is_published": True,
                    "seo_title": data["title"],
                    "seo_description": data["subtitle"],
                },
            )
            post.tags.add(*[tags[slug] for slug in tag_slugs])

    def seed_bookmarks(self):
        groups = [
            (
                "Django Essentials",
                1,
                [
                    ("Django Documentation", "https://docs.djangoproject.com/", "Primary reference for Django features."),
                    ("Django Deployment Checklist", "https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/", "A useful final check before production."),
                ],
            ),
            (
                "Deployment",
                2,
                [
                    ("Render Docs", "https://render.com/docs", "Hosting, environment variables, disks, and deployment behavior."),
                    ("WhiteNoise", "https://whitenoise.readthedocs.io/", "Static file serving for Python web apps."),
                ],
            ),
        ]
        for title, order, bookmarks in groups:
            group, _ = BookmarkGroup.objects.get_or_create(
                title=title,
                defaults={"order": order, "is_active": True},
            )
            for bookmark_order, (label, url, description) in enumerate(bookmarks, start=1):
                Bookmark.objects.get_or_create(
                    group=group,
                    label=label,
                    defaults={
                        "url": url,
                        "description": description,
                        "order": bookmark_order,
                        "is_active": True,
                    },
                )

    def seed_social_links(self):
        links = [
            ("GitHub", "https://github.com/", 1),
            ("LinkedIn", "https://www.linkedin.com/", 2),
            ("Email", "mailto:hello@example.com", 3),
        ]
        for label, url, order in links:
            SocialLink.objects.get_or_create(
                label=label,
                defaults={"url": url, "order": order, "is_active": True},
            )

    def seed_navigation(self, pages):
        nav_items = [
            ("About", pages.get("about"), 1),
            ("Now", pages.get("now"), 2),
        ]
        for label, page, order in nav_items:
            if page:
                NavigationItem.objects.get_or_create(
                    label=label,
                    defaults={"page": page, "order": order, "is_active": True},
                )
