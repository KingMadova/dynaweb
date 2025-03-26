from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy 
from django.http import HttpRequest, HttpResponseRedirect
from django.core.mail import send_mail

from .models import Category, Post, Comment

from django.contrib.auth.decorators import login_required
from .forms import PostForm, EditForm, CommentForm  # Utilisez CommentForm au lieu de AddCommentForm


def contact(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        service = request.POST.get("service")
        message = request.POST.get("message")
        
        subject = f"Message de {name}"
        body = f"""
            Nom : {name}
            Email : {email}
            Téléphone : {phone}
            Service : {service}
            Message : {message}
        
        """
        send_mail(subject, body, email, ['gae@gmail.com'])
        
        return redirect(reverse('confirmation') + f'?name={name}&email={email}')
    return render(request, 'contact.html')



def confirmation_view(request : HttpRequest):
    name = request.GET.get('name')
    email = request.GET.get('email')
    
    context = {'name': name, 'email': email}
    return render(request, 'confirmation.html', context)

# FORMULAIRE DE CONTACT


def about(request):
    return render(request, 'about.html')

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
        
    return HttpResponseRedirect(reverse('article_detail', args=[str(pk)]))


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    # ordering = ['-post_date']
    ordering = ['-id']

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        main_post = Post.objects.filter(Main_Post=True)
        tendance = Post.objects.filter(section='Tendance').order_by('-id')
        category = Post.objects.filter(section='Category').order_by('-id')
        small_cat = Post.objects.filter(section='Small_cat').order_by('-id')
        regular = Post.objects.filter(section='Regular').order_by('-id')
        dernier_post = Post.objects.filter(section='Dernier_Post').order_by('-id')
        context = {
            'cat_menu': cat_menu,
            'main_post': main_post,
            'tendance': tendance,
            'category': category,
            'small_cat': small_cat,
            'regular': regular,
            'dernier_post': dernier_post,
        }
        return context


def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    return render(request, 'category_list.html', {'cat_menu_list':cat_menu_list})
    

def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats.replace('-', ' '))
    return render(request, 'categories.html', {'cats':cats.title().replace('-', ' '), 'category_posts':category_posts})
    
    
class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'  
    
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        
        context["cat_menu"] = cat_menu
        context["total_likes"] = total_likes
        context["liked"] = liked
        
        return context
    
def article_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
        # Récupérer les 5 derniers articles publiés
    small_cat = Post.objects.filter(status='1').order_by('-post_date')[:5]
    
    return render(request, 'article_detail.html', {'post': post, 'small_cat': small_cat})


def search_articles(request):
    query = request.GET.get('q')  # Récupère le texte de recherche
    results = []

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(category__icontains=query), status='1'
        ).distinct()  # Recherche par titre ou catégorie

    return render(request, 'search_results.html', {'query': query, 'results': results})





class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'add_post.html'  
    fields = ('title', 'title_tag', 'header_image', 'body', 'category', 'snippet', 'section', 'status','Main_Post')

    def test_func(self):
        return self.request.user.is_superuser  # Seul l'admin peut poster

    def handle_no_permission(self):
        return redirect('home')  # Redirige les non-admins vers l'accueil

    def form_valid(self, form):
        form.instance.author = self.request.user  # Ajoute l'utilisateur connecté
        return super().form_valid(form)


class AddCommentView(CreateView):
    model = Comment
    template_name = 'add_comment.html'
    fields = ('name', 'body')

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('article_detail', kwargs={'pk': self.kwargs['pk']})  



class AddCategoryView(CreateView):
    model = Category
    # form_class = PostForm
    template_name = 'add_category.html'  
    fields = '__all__'
    # fields = ('title', 'body')
    
class UpdatePostView(UserPassesTestMixin, UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'
    # fields = ['title', 'title_tag', 'body']
    
    def test_func(self):
        return self.request.user.is_superuser
    
class DeletePostView(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        return self.request.user.is_superuser