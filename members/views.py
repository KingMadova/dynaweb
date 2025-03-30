from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.views.generic import DetailView, CreateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.db.models import Count
from django.contrib.auth.models import User
from app.models import Comment  # Importez votre modèle Comment



from app.models import Profile
from .forms import PasswordChangingForm, ProfilePageForm, SignUpForm, EditProfileForm

class CreateProfilePageView(CreateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = 'registration/create_user_profile_page.html'
    # fields = '__all__'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditProfilePageView(generic.CreateView):
    model = Profile
    template_name = 'registration/edit_profile_page.html'
    fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'twitter_url', 'instagram_url', 'pinterest_url']
    success_url = reverse_lazy('home')


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        
        # Obtenez les statistiques de l'utilisateur en utilisant les bons related_names
        user_stats = User.objects.filter(
            pk=profile.user.pk
        ).annotate(
            post_count=Count('posts', distinct=True),  # Utilisez 'posts' au lieu de 'post'
            comment_count=Count('comments', distinct=True)
        ).first()
        
        context.update({
            'page_user': profile,
            'post_count': user_stats.post_count if user_stats else 0,
            'comment_count': user_stats.comment_count if user_stats else 0,
            'author': profile.user  # Ajout de l'utilisateur au contexte
        })
        return context


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    # form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')
    # success_url = reverse_lazy('home')

def password_success(request):
    return render(request, 'registration/password_success.html', {})

class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

def logout_view(request):
    logout(request)
    return redirect('home') 