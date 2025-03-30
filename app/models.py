from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=191)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(blank=True, null=True, upload_to='images/profile/')
    website_url = models.CharField(max_length=191, blank=True, null=True)
    facebook_url = models.CharField(max_length=191, blank=True, null=True)
    twitter_url = models.CharField(max_length=191, blank=True, null=True)
    instagram_url = models.CharField(max_length=191, blank=True, null=True)
    pinterest_url = models.CharField(max_length=191, blank=True, null=True)

    def __str__(self):
        return str(self.user)
    
    def get_absolute_url(self):
        return reverse('home')
    
    def get_comment_count(self):
        return self.user.comment_set.count()
    
    def get_post_count(self):
        return self.user.post_set.count()
    
    def get_last_activity(self):
        last_post = self.user.post_set.order_by('-date_posted').first()
        last_comment = self.user.comment_set.order_by('-date_added').first()
        
        if last_post and last_comment:
            return max(last_post.date_posted, last_comment.date_added)
        return last_post.date_posted if last_post else last_comment.date_added


class Post(models.Model):
    STATUS = (
        ('0', 'Draft'),
        ('1', 'Published'),
    )
    SECTION = (
        
        ('Main_Post', 'Main_Post'),
        ('Tendance', 'Tendance'),
        ('Regular', 'Regular'),
        ('Category', 'Category'),
        ('Small_cat', 'Small_cat'),
        ('Dernier_Post', 'Dernier_Post')
    )

    title = models.CharField(max_length=191)
    header_image = models.ImageField(blank=True, null=True, upload_to='images/')
    title_tag = models.CharField(max_length=191)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = RichTextField(blank=True, null=True)
    post_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=191, default='')
    snippet = models.CharField(max_length=191)
    likes = models.ManyToManyField(User, related_name='blog_posts', blank=True)
    section = models.CharField(choices=SECTION, max_length=200)
    status = models.CharField(choices=STATUS, max_length=200)  
    Main_Post = models.BooleanField(default=False) 
    
    def total_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        # return reverse('article_detail', args=(str(self.id)))
        return reverse('home')

    @property
    def comment_count(self):
        return self.comments.count()  # Utilise le related_name  # Compte
    

# models.py
class Comment(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='comments'  # Définissez explicitement le related_name
    )
    post = models.ForeignKey(
        'Post',  # ou votre modèle Post
        on_delete=models.CASCADE,
        related_name='comments'  # Ceci crée la relation inverse
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    
    def total_likes(self):
        return self.likes.count()



class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
