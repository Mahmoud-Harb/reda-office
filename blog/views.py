from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        UserPassesTestMixin)
from django.urls import reverse_lazy, reverse
from .models import Post, Reply

import re


def index(request):
    context = {
        "posts": Post.objects.all()
    }
    return render(request, 'blog/index.html', context)


class SearchListView(ListView):
    template_name = 'blog/search_results.html'
    context_object_name = 'results'
    paginate_by = 30

    def get_queryset(self):
        results = []
        search_word = self.request.GET.get('search')
        all_posts = Post.objects.all()
        for post in all_posts:
            if re.search('%s' % search_word, '%s' % post, flags=re.I) and\
                search_word != "":
                results.append(post)
        return results


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # display the reply form in blog list view
        reply_form = ReplyCreateView()
        context['reply_form'] = reply_form.get_form_class()
        return context



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'file_upload', 'image_upload','content', ]
    

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'file_upload', 'image_upload', 'content',]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = Reply
    fields = ['reply']
    # success_url = '/blog/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        return super().form_valid(form)
    # """ get the page section by it's id and redirect to
    #     it after reply get created >> example '/blog/#post-5' 
    #     which 'post-5' is the id of the section containig the 
    #     post get replied to """     
    def get_success_url(self, **kwargs):
        # return reverse_lazy('blog:post-detail', kwargs={"pk": self.kwargs['pk']})
        return f'/blog/post/{self.kwargs["pk"]}#reply-form'


class PostListView(ListView):
    model = Post
    template_name = 'blog/blog-index.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # display the reply form in blog list view
        reply_form = ReplyCreateView()
        context['reply_form'] = reply_form.get_form_class()
        return context
