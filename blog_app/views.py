from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from .models import Blog, Comment, Like, BlogShare
from django.core.mail import send_mail


class UserRegistrationView(View):
    template_name = 'registration/register.html'

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            login(request, user)
            return redirect('blog_list')
        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class BlogListView(View):
    template_name = 'blog-list.html'
    paginate_by = 5

    def get(self, request):
        blogs = Blog.objects.all()
        paginator = Paginator(blogs, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'page_obj': page_obj})

class BlogDetailView(View):
    template_name = 'blog/blog_detail.html'

    def get(self, request, blog_id):
        blog = Blog.objects.get(pk=blog_id)
        comments = Comment.objects.filter(blog=blog)
        like = Like.objects.filter(blog=blog).count()
        share = BlogShare.objects.filter(blog=blog).count()
        return render(
            request,self.template_name, {
                'blog': blog,
                'comments': comments,
                "like":like,
                "share":share
                })


class AddCommentView(View):
    @method_decorator(login_required)
    def post(self, request, blog_id):
        text = request.POST.get('comment_text')
        blog = Blog.objects.get(pk=blog_id)
        Comment.objects.create(blog=blog, user=request.user, text=text)
        return redirect('blog_detail', blog_id=blog_id)

class LikeCommentView(View):
    @method_decorator(login_required)
    def post(self, request, comment_id):
        comment = Blog.objects.get(pk=comment_id)
        Like.objects.create(user=request.user, comment=comment)
        return redirect('blog_detail', blog_id=comment.blog.id)


class ShareBlogView(View):
    template_name = 'blog/share_blog.html'

    @method_decorator(login_required)
    def post(self, request, blog_id):
        blog = Blog.objects.get(pk=blog_id)
        email = request.POST.get('email')
        
        # Save the shared blog information in the BlogShare model
        BlogShare.objects.create(blog=blog, email=email)

        # Send email
        subject = f"Check out this blog: {blog.title}"
        message = f"Hi,\n\nI thought you might be interested in reading this blog:\n\n{blog.title}\n\n{blog.content}"
        from_email = "your@example.com"
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        return redirect('blog_detail', blog_id=blog_id)
