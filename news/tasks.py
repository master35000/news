from celery import shared_task
import datetime
from news.models import Post, Category
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from NewsPaper import settings

@shared_task
def weekly_mailing():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(datetime_in__gte=last_week)
    categories = set(posts.values_list('pcategory__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string('daily_post.html', {'link': settings.SITE_URL, 'posts':posts})
    msg = EmailMultiAlternatives(subject='Публикации за неделю', body='', from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_new_post(pk):
    instance = Post.objects.get(pk=pk)
    subscribers_emeils = []
    subject = instance.title
    html_content = render_to_string('post_created_email.html',{'text': instance.preview, 'link': f'{settings.SITE_URL}/posts/{pk}'})

    for cat in instance.pcategory.all():
        subscribers = cat.subscribers.all()
        subscribers_emeils += [s.email for s in subscribers]

    for email in subscribers_emeils:
        msg = EmailMultiAlternatives(subject, body='', from_email=settings.DEFAULT_FROM_EMAIL, to=[email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
