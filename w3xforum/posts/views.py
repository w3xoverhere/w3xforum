from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Category, Image
from .forms import PostForm
from django.core.paginator import Paginator


class PostsList(ListView):
    queryset = Post.objects.filter(is_published=True)
    paginate_by = 3
    template_name = "posts/posts_list.html"


class PostDetail(DetailView):
    queryset = Post.objects.all()
    context_object_name = 'current_post'
    template_name = 'posts/post_detail.html'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('category_slug', None)
        pk = self.kwargs.get('post_pk', None)
        try:
            return Post.objects.get(category__slug=slug, pk=pk)
        except:
            raise Http404('Post does not exist')


def post_detail(request, category_slug, post_pk):
    post = get_object_or_404(Post, category__slug=category_slug, pk=post_pk)
    context = {
        'current_post': post,
    }
    return render(request, "posts/post_detail.html", context=context)


def post_add(request):
    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('imgs')
        if form.is_valid():
            category = form.cleaned_data['category']
            user = request.user
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            post_obj = Post.objects.create(category=category, title=title, content=content, author=user)
            for f in files:
                Image.objects.create(post=post_obj, imgs=f)
            messages.success(request, 'Вы отправили пост на проверку :)')
        else:
            messages.error(request, 'Ошибка отправки!')
    else:
        form = PostForm()
    return render(request, 'posts/post_add.html', context={'form': form})


class CategoryList(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = "posts/categories_list.html"


def category_detail(request, category_slug):
    cat = get_object_or_404(Category, slug=category_slug)
    posts = cat.post_set.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "category": cat,
        'page_obj': page_obj
    }
    return render(request, "posts/category_detail.html", context=context)
