from django.shortcuts import render, get_object_or_404
from requests import request
from .models import Post, Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import PostForm
from django.urls import reverse_lazy
from .filters import PostFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from .models import PostCategory
import requests
from .tasks import send_new_post

# Create your views here.

class NewsList(ListView):
    model = Post
    ordering = '-datetime_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class NewsSearch(ListView):
    model = Post
    ordering = '-datetime_in'
    template_name = 'posts_search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail (DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class PostCreate(LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/posts/news/create/':
            post.post_type = 'NE'
        post.save()
        send_new_post.delay(post.pk)
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def dispatch(self, request, *args, **kwargs ):
        post = self.get_object()

        if self.request.path == f'/posts/news/{post.pk}/edit/' and post.post_type != 'NE':
            return render(self.request, 'invalid_news_edit.html')
        elif self.request.path == f'/posts/articles/{post.pk}/edit/' and post.post_type != 'AR':
            return render(self.request, 'invalid_articles_edit.html')
        return super(PostUpdate, self).dispatch(request, *args, **kwargs)


class PostDelete(LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs ):
        post = self.get_object()

        if self.request.path == f'/posts/news/{post.pk}/delete/' and post.post_type != 'NE':
            return render(self.request, 'invalid_news_delete.html')
        elif self.request.path == f'/posts/articles/{post.pk}/delete/' and post.post_type != 'AR':
            return render(self.request, 'invalid_articles_delete.html')
        return super(PostDelete, self).dispatch(request, *args, **kwargs)


class CategoryListView(NewsList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.pcategory = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(pcategory=self.pcategory).order_by('-datetime_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.pcategory.subscribers.all()
        context['category'] = self.pcategory
        return context

@login_required()
def subscribe(request, pk):
    user=request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Вы успешно подписались на рассылку категории'
    return render(request,'subscribe.html', {'category':category, 'message':message})


@login_required
@csrf_protect
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    message = 'Вы успешно отписались от рассылки  категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})