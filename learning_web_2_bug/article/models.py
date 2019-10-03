from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from slugify import slugify
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey

class ArticleColumn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='article_column')
    column = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.column
    
class ArticleTag(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tag")
    tag = models.CharField(max_length=500)
    
    def __str__(self):
        return self.tag


class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn,on_delete=models.CASCADE,related_name="article_column")
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(auto_now=True)
    users_like = models.ManyToManyField(User,
            related_name="articles_like", blank=True)
    article_tag = models.ManyToManyField(ArticleTag, related_name="article_tag", blank=True)
    article_writer = models.CharField(max_length=500)
    person_likes = models.PositiveIntegerField(default=0)

    
    class Meta:
        ordering = ("-created",)
        index_together = (("id", "slug"),)
    
    def __str__(self):
        return self.title
    
    def save(self,*args,**kargs):
        self.slug = slugify(self.title)
        super(ArticlePost,self).save(*args, **kargs)
    
    def get_absolute_url(self):
        return reverse("blog:blog_detail",args=[self.id,self.slug])
    
    def get_url_path(self):
        return reverse("blog:blog_detail",args=[self.id, self.slug])
        
class Comment(MPTTModel):
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE,
                                related_name="comments")
    commentator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
        
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )
    
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replyers"
    )
        
    
    class MPTTMeta:
        order_insertion_by = ["created"]
        
    def get_nodeid(self):
        return  self.id
    
        
    #def __str__(self):
        #return"Comment by {0} on{1}".format(self.commentator.username, self.article)
