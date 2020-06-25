from django.http import HttpResponse
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404, redirect
import random
from .forms import PostForm


def index(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    number = random.randrange(0, 100)
    context = {
        'posts':posts,
    }

    return render(request, "rss_news/index.html", context)

def post_detail(request, pk):
    Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'rss_news/post_detail.html', {'post': post})

def post_new(request):
    #Первая: когда мы только зашли на страницу и хотим получить пустую форму. Вторая: когда мы возвращаемся к представлению со всей информацией, которую мы ввели в форму.
    if request.method == "POST":
        form = PostForm(request.POST)
        # корректна ли форма (все ли необходимые поля заполнены и не отправлено ли некорректных значений)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'rss_news/post_edit.html', {'form':form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'rss_news/post_edit.html', {'form': form})