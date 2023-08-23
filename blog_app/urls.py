from django.urls import path
from .views import BlogListView, BlogDetailView, UserRegistrationView, CustomLoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('blog/<int:blog_id>/', BlogDetailView.as_view(), name='blog_detail'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)