from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
                                    ListView,
                                    DetailView,
                                    CreateView,
                                    UpdateView,
                                    DeleteView, )
from blog.models import Post


class PostListView(ListView): #list every post object create by each user

    model = Post #from post model

    template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html

    context_object_name = 'posts'

    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post


class PostCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):

    model = Post

    fields = ['title','content']

    template_name_suffix = '_update_form'

    login_url = '/login/'

    success_message = "Post has been created successfully!"
#---------------------------------#

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Post

    fields = ['title','content']

    template_name_suffix = '_update_form'

    login_url = '/login/'


    def form_valid(self, form):

        form.instance.author = self.request.user

        return super().form_valid(form)

    def test_func(self):

        post = self.get_object()

        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(SuccessMessageMixin, LoginRequiredMixin,
                     UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' #take it to the homepage
    success_message = "Post has been deleted" #todo: find a way to provide feedback
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

#---------------------------------#
def about(request):

    response = "blog/about.html"

    return render(request, response, {'title':'Blog'})


def contact_us(request):

    response = "blog/contact.html"

    return render(request, response, {'title':'Contact'})
#---------------------------------#
