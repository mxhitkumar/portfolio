from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("blog/", views.BlogListView.as_view(), name="blog"),
    path("blog/<slug:slug>/", views.BlogDetailView.as_view(), name="blog_detail"),
    path("work/", views.WorkView.as_view(), name="work"),
    path("projects/", views.ProjectsView.as_view(), name="projects"),
    path("bookmarks/", views.BookmarksView.as_view(), name="bookmarks"),
    path("tags/", views.TagsView.as_view(), name="tags"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("search.json", views.search_index, name="search_index"),
    path("pages/<slug:slug>/", views.PageDetailView.as_view(), name="page_detail"),
]
