from . import views as view
from django.urls import path
from django.contrib.auth import views as auth_views
from userMgt import views as userMgtViews

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='userMgt/login.html'), name='login-home'),
    path('blog/', view.PostListView.as_view(), name='blog-home'),
    path('user/<str:username>/', view.UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', view.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', view.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', view.UpdatePostView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', view.PostDeleteView.as_view(), name='post-delete'),
    path('about/', view.about, name='blog-about'),
    path('contact/', view.contact_us, name='blog-contact'),
]
