from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    RedirectView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import PostCreateModelForm
from .mixins import AuthorAccessMixin


# Create your views here.
def index_view(request):
    return render(request, "index.html", {"type": "fbv"})


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.all()
        context["type"] = "cbv"
        return context


class RedirectToMaktabkhooneh(RedirectView):
    url = "https://maktabkhooneh.org/"

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"])
        print(post)
        return super().get_redirect_url(*args, **kwargs)


class PostListView(ListView):
    model = Post
    template_name = "blog/posts_list.html"
    paginate_by = 2

    def get_queryset(self):
        return super().get_queryset().order_by("published")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_kwarg"] = self.page_kwarg
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "blog/post_detail.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateModelForm
    login_url = reverse_lazy("blog:login-view")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_type"] = "Create"
        return context


class PostEditView(LoginRequiredMixin, AuthorAccessMixin, UpdateView):
    model = Post
    form_class = PostCreateModelForm
    login_url = reverse_lazy("blog:login-view")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_type"] = "Update"
        return context


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("blog:posts-list-view")
    login_url = reverse_lazy("blog:login-view")


class PostListAPIView(TemplateView):
    template_name = "blog/post_list_api.html"
