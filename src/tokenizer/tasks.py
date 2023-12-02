from celery import Celery

celery = Celery("tokenizer", broker="redis://127.0.0.1:6379")

celery.conf.beat_schedule = {
    'tokenize_ml_keywords_600_seconds': {
        'task': 'tokenize_from_db.main',
        'schedule': 300,
        'args': ("temp_article", ),  #
    },
}
