from django.db import models
from .resources import ARTICLE, AN
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

# Create your models here.

class Author (models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    rating = models.IntegerField(default = 0)

    def __str__ (self):
        return f'{self.user}'

    def update_rating(self):
        postRating = self.post_set.aggregate(pRating=Sum('rating'))
        pr = 0
        pr += postRating.get('pRating')

        commentRating = self.user.comment_set.aggregate(cRating=Sum('rating'))
        cr=0
        cr += commentRating.get('cRating')

        self.rating = pr * 3 + cr
        self.save()


class Category (models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User,blank=True, null=True, related_name='categories')

    def __str__ (self):
        return f'{self.name}'


class Post (models.Model):
    author = models.ForeignKey('Author', on_delete = models.CASCADE)
    post_type = models.CharField(max_length=2, choices= AN, default=ARTICLE)
    datetime_in = models.DateTimeField(auto_now_add = True)
    pcategory = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()


    def dislike(self):
        self.rating -= 1
        self.save()

    def preview (self):
        return f'{self.text[:123]} ...'

    def __str__ (self):
        return f'{self.author.user} - {self.title}'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])


class PostCategory (models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment (models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    datetime_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


