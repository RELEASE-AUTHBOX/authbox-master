from celery import Celery
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','django_authbox.settings')
REDIS_SOCKET_PATH='/home/authboxw/tmp/redis.sock'
CELERY_BROKER_URL=f"redis+socket://{REDIS_SOCKET_PATH}?virtual_host=0"
CELERY_RESULT_BACKEND=f"redis+socket://{REDIS_SOCKET_PATH}?virtual_host=1"
app=Celery('tasks',broker=CELERY_BROKER_URL)
app.autodiscover_tasks()
CELERY_BEAT_SCHEDULE={'cleanup_task':{'task':'tasks.cleanup','schedule':6e1}}