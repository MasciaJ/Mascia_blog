from django.shortcuts import render

from blog.models import Post


def portfolio(request):
    posts = Post.objects.prefetch_related("categories").order_by("-created_on")
    return render(request, "portfolio/index.html", {"posts": posts})