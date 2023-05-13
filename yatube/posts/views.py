from common.views import TitleMixin
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import PostForm
from .models import Group, Post


class IndexListView(TitleMixin, ListView):
    paginate_by = 5
    model = Post
    template_name = 'posts/index.html'
    title = 'Последние обновления'

    
class PostListView(ListView):
    paginate_by = 5
    model = Post
    template_name = 'posts/group_list.html'

    def get_queryset(self):
        queryset = super(PostListView, self).get_queryset()
        slug = self.kwargs.get('slug')
        group = Group.objects.get(slug=slug)
        group_id = group.id
        return queryset.filter(group=group_id)

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['group'] = Group.objects.get(slug=self.kwargs.get('slug'))
        slug = self.kwargs.get('slug')
        context['title'] = f'Посты группы {slug}'
        return context
    

class ProfileListView(ListView):
    paginate_by = 5
    model = Post
    template_name = 'posts/profile.html'

    def get_queryset(self):
        queryset = super(ProfileListView, self).get_queryset()
        user = self.kwargs.get('pk')
        return queryset.filter(author=user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Посты автора {self.request.user}'
        context['len'] = len(Post.objects.filter(author=self.kwargs.get('pk')))
        return context
    

class PostCreateView(TitleMixin, CreateView):    
    model = Post
    fields = ('text', 'group')
    template_name = 'posts/post_create.html'
    success_url = reverse_lazy('posts:index')
    title = 'Новый пост'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super(PostCreateView, self).form_valid(form)
    

class PostDetailView(TitleMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    title = 'Детали поста'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['len'] = len(Post.objects.filter(author=self.object.author))
        return context
    

class PostUpdateView(TitleMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_update.html'
    title = 'Изменение поста'
    
    def get_success_url(self):
        return reverse_lazy('posts:post_detail', args=(self.kwargs.get('pk'),))
    

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('posts:index')
