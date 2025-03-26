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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
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

    def comment_count(self):
        return self.comments.count()  # Compte
    

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=191)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)



class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
