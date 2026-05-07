from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, TemplateView

from apps.cms.models import HomePage, Service
from apps.contact.forms import ContactForm

from .models import BlogPost, BookmarkGroup, Page, Project, SocialLink, Tag, WorkItem


class PublishedBlogMixin:
    model = BlogPost

    def get_queryset(self):
        return (
            BlogPost.objects.filter(is_published=True)
            .prefetch_related("tags")
            .order_by("-published_at", "-created_at")
        )


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        home = HomePage.load()
        context.update(
            {
                "home": home,
                "seo_obj": home,
                "page_title": home.seo_title or home.hero_title,
                "posts": BlogPost.objects.filter(is_published=True).order_by(
                    "-published_at", "-created_at"
                )[:10],
                "services": Service.objects.filter(is_active=True),
            }
        )
        return context


class BlogListView(PublishedBlogMixin, ListView):
    template_name = "pages/blog.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Blog"
        return context


class BlogDetailView(PublishedBlogMixin, DetailView):
    template_name = "pages/blog_detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seo_obj"] = self.object
        context["page_title"] = self.object.seo_title or self.object.title
        return context


class PageDetailView(DetailView):
    model = Page
    template_name = "pages/page.html"
    context_object_name = "page"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Page.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seo_obj"] = self.object
        context["page_title"] = self.object.seo_title or self.object.title
        return context


class WorkView(TemplateView):
    template_name = "pages/work.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Work"
        context["work_items"] = WorkItem.objects.filter(is_active=True)
        return context


class ProjectsView(TemplateView):
    template_name = "pages/projects.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Projects"
        context["projects"] = Project.objects.filter(is_active=True).prefetch_related("links")
        return context


class BookmarksView(TemplateView):
    template_name = "pages/bookmarks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Bookmarks"
        context["bookmark_groups"] = BookmarkGroup.objects.filter(
            is_active=True
        ).prefetch_related("bookmarks")
        return context


class TagsView(TemplateView):
    template_name = "pages/tags.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Tags"
        context["tags"] = Tag.objects.prefetch_related("posts")
        return context


class ContactView(TemplateView):
    template_name = "pages/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Contact"
        context.setdefault("form", ContactForm())
        context["social_links"] = SocialLink.objects.filter(is_active=True)
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f"{request.path}?success=1")
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(success=request.GET.get("success") == "1")
        return self.render_to_response(context)


def search_index(request):
    documents = []
    for post in BlogPost.objects.filter(is_published=True).prefetch_related("tags"):
        documents.append(
            {
                "title": post.title,
                "url": post.get_absolute_url(),
                "content": " ".join([post.subtitle, post.body]),
                "tags": [tag.name for tag in post.tags.all()],
            }
        )
    for page in Page.objects.filter(is_published=True):
        documents.append(
            {
                "title": page.title,
                "url": page.get_absolute_url(),
                "content": " ".join([page.intro, page.body]),
                "tags": [],
            }
        )
    return JsonResponse({"documents": documents})


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def healthcheck(request):
    return JsonResponse({"status": "ok"})
