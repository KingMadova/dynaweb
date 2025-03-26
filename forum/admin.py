from django.contrib import admin
from .models import ForumCategory, Topic, Reply

class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'total_upvotes', 'total_downvotes')
    list_filter = ('category', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('created_at',)
    filter_horizontal = ('upvotes', 'downvotes')

    def total_upvotes(self, obj):
        return obj.upvotes.count()
    total_upvotes.short_description = 'Upvotes'

    def total_downvotes(self, obj):
        return obj.downvotes.count()
    total_downvotes.short_description = 'Downvotes'

class ReplyAdmin(admin.ModelAdmin):
    list_display = ('topic', 'author', 'created_at', 'total_likes')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__username', 'topic__title')
    readonly_fields = ('created_at',)
    filter_horizontal = ('likes',)

    def total_likes(self, obj):
        return obj.likes.count()
    total_likes.short_description = 'Likes'

# Enregistrement des modèles
admin.site.register(ForumCategory, ForumCategoryAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Reply, ReplyAdmin)