from celery import Celery
import os
from dotenv import load_dotenv
from app.config.settings_config import RedisConfig
# Load environment variables
load_dotenv()

# Celery configuration
celery_app = Celery(
    'flatizo',
    broker=f"redis://{RedisConfig.REDIS_HOST}:{RedisConfig.REDIS_PORT}",
    backend=f"redis://{RedisConfig.REDIS_HOST}:{RedisConfig.REDIS_PORT}",
    include=['app.tasks.email']
)

# Celery configuration settings
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Kolkata',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    task_soft_time_limit=25 * 60,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Export the task decorator
task = celery_app.task
