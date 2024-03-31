import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    'weekly': {
        'task': 'news.tasks.weekly_mailing',
        'schedule': crontab(minute='0', hour='0', day_of_week='monday')

    },
}



