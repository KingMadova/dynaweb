from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .models import Topic, Reply, ForumCategory
from .forms import TopicForm, ReplyForm
from django.db.models import Count



def is_moderator(user):
    return user.is_authenticated and user.is_superuser

class ForumListView(ListView):
    model = Topic
    template_name = "forum/forum_list.html"
    context_object_name = "topics"

    def get_queryset(self):
        return Topic.objects.select_related('author', 'category').prefetch_related('replies')


class TopicDetailView(DetailView):
    model = Topic
    template_name = "forum/topic_detail.html"
    context_object_name = "topic"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.topic = self.object
            reply.author = request.user
            reply.save()
        return redirect('forum:topic_detail', pk=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReplyForm()
        return context

class CreateTopicView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = "forum/create_topic.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('forum:topic_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ForumCategory.objects.all()
        return context

@login_required
def add_reply(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.topic = topic
            reply.save()
            return redirect('forum:topic_detail', pk=topic_id)
    else:
        form = ReplyForm()
    return render(request, "forum/add_reply.html", {"form": form, "topic": topic})

@user_passes_test(is_moderator)
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    topic.delete()
    return redirect("forum:forum_list")

@login_required
def upvote_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.user in topic.upvotes.all():
        topic.upvotes.remove(request.user)
    else:
        topic.upvotes.add(request.user)
        topic.downvotes.remove(request.user)
    return redirect('forum:forum_list')

@login_required
def downvote_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.user in topic.downvotes.all():
        topic.downvotes.remove(request.user)
    else:
        topic.downvotes.add(request.user)
        topic.upvotes.remove(request.user)
    return redirect('forum:forum_list')

@login_required
def like_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    if request.user in reply.likes.all():
        reply.likes.remove(request.user)
    else:
        reply.likes.add(request.user)
    return redirect(request.META.get("HTTP_REFERER", "forum:forum_list"))


def topic_list(request):
    category_id = request.GET.get('category')
    
    topics = Topic.objects.all()
    if category_id:
        topics = topics.filter(category_id=category_id)  # Assurez-vous que le champ s'appelle bien 'category' dans le modèle Topic
    
    categories = ForumCategory.objects.annotate(topic_count=Count('topic'))  # Modifier ici
    
    return render(request, 'forum/topic_list.html', {
        'topics': topics,
        'categories': categories,
    })