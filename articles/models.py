from django.db import models
from django.utils import timezone


class Article(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=50, unique=True)
    body = models.TextField(max_length=1000)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Comment(models.Model):

    class Meta:
            verbose_name = "Comment"
            verbose_name_plural = "Commentss"

    nick = models.CharField(max_length=100)
    body = models.TextField(max_length=500)
    likes = models.IntegerField(default=0)
    spam = models.IntegerField(default=0)
    article = models.ForeignKey(Article, related_name="article_comments")
    comment = models.ForeignKey('self', blank=True, null=True, related_name='children')
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        output = "%s_%s" % (self.article, self.nick)
        return output
