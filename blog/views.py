from django.shortcuts import render,get_object_or_404,redirect
from.models import Post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin ,UserPassesTestMixin
from django.contrib.auth.models import User
from users.forms import CommentForm
from django.contrib import messages
def home(request):
    context={'posts':Post.objects.all()}
    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model=Post
    
    template_name='blog/home.html'
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=5
    
class UserPostListView(ListView):
    model=Post
    
    template_name='blog/user_posts.html'
    context_object_name='posts'
    paginate_by=5    
     
    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')                       
                                      
        
class PostDetailView(DetailView): 
    model=Post
    
    template_name = 'blog/post_detail.html'
    
   
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        post = get_object_or_404(Post,pk=self.kwargs.get('pk'))
        context['comments'] = post.comments.all().order_by('-created_on') 
        return context
    
        
    
    
        
        
    
    

def add_comment_to_post(request,pk):
    template_name = 'blog/add_comment_to_post.html'
    post = get_object_or_404(Post,pk=pk)
    #comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            messages.success(request, f'Your comment has been posted')
            return redirect('post-detail',pk=post.pk)
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'comment_form': comment_form})
                                           
    
    
class PostCreateView( LoginRequiredMixin,CreateView):
    model=Post  
    
    fields=['title','content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post  
    
    fields=['title','content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
         
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
        
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post 
    #success_url=reverse_lazy('blog-home')
    success_url='/'
    
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
    
        
    
    
    
    
    
    
    
        



def about(request):
    context={'title':'Blog-about'}
    return render(request,'blog/about.html',context)
 