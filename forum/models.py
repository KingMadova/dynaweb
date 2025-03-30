from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save

class ForumCategory(models.Model):
    name = models.CharField(max_length=191, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Forum Categories"

    def __str__(self):
        return self.name

def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = ForumCategory.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = f"{slug}-{qs.first().id}"
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_category_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_category_receiver, sender=ForumCategory)

class Topic(models.Model):
    title = models.CharField(max_length=191, unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE, related_name='topics')
    # category = models.ForeignKey(ForumCategory, on_delete=models.PROTECT)  # Utilisez ForumCategory ici
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(User, related_name="upvoted_topics", blank=True)
    downvotes = models.ManyToManyField(User, related_name="downvoted_topics", blank=True)

    def total_upvotes(self):
        return self.upvotes.count()

    def total_downvotes(self):
        return self.downvotes.count()
    
    def __str__(self):
        return self.title

class Reply(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="replies")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_replies", blank=True)
    parent_reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    @property
    def total_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return f"Réponse de {self.author} à {self.topic.title}"