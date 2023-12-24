from celery import Celery, shared_task
from tokenizer.tokenize_from_db import main
from parse_news.celery_funcs import launch_spider

# clry_tknzr = Celery("tokenizer", broker="redis://127.0.0.1:6379")
clry_spdr = Celery("parse_news", broker="redis://127.0.0.1:6379")

# clry_tknzr.conf.beat_schedule = {'tokenize_ml_keywords_60m': {'task': 'tokenizer.tokenize_from_db.main',
#                                                               'schedule': 60 * 60,
#                                                               'args': ("temp_article",),
#                                                               },
#                                  }

clry_spdr.conf.beat_schedule = {'launch_naked_science_60m': {'task': 'parse_news.celery_funcs.launch_spider',
                                                             'schedule': 60 * 60 + 1,
                                                             'args': ("naked-science.ru", "celery"),  #
                                                             },
                                'launch_cnews_60m': {'task': 'parse_news.celery_funcs.launch_spider',
                                                     'schedule': 60 * 30 + 2,
                                                     'args': ("cnews.ru", "celery"),  #
                                                     },
                                'launch_fontanka_60m': {'task': 'parse_news.celery_funcs.launch_spider',
                                                        'schedule': 60 * 45 + 3,
                                                        'args': ("fontanka.ru", "celery"),  #
                                                        },
                                'launch_3dnews_60m': {'task': 'parse_news.celery_funcs.launch_spider',
                                                      'schedule': 60 * 60 + 4,
                                                      'args': ("3dnews.ru", "celery"),  #
                                                      },
                                'launch_forbes_60m': {'task': 'parse_news.celery_funcs.launch_spider',
                                                      'schedule': 60 * 60 + 5,
                                                      'args': ("forbes.ru", "celery"),  #
                                                      },
                                'launch_knife_60m': {'task': 'parse_news.celery_funcs.launch_spider',
                                                     'schedule': 60 * 60 + 6,
                                                     'args': ("knife.media", "celery"),  #
                                                     },
                                'launch_nplus1_60m': {'task': 'parse_news.celery_funcs.launch_spider',
                                                      'schedule': 60 * 60 + 7,
                                                      'args': ("nplus1.ru", "celery"),  #
                                                      },
                                'launch_portal-kultura_60m': {'task': 'parse_news.celery_funcs.launch_spider',
                                                              'schedule': 60 * 60 + 8,
                                                              'args': ("portal-kultura.ru", "celery"),  #
                                                              },
                                'launch_sdelanounas_60m': {'task': 'parse_news.celery_funcs.launch_spider',
                                                           'schedule': 60 * 60 + 9,
                                                           'args': ("sdelanounas.ru", "celery"),  #
                                                           },
                                'launch_snob_60m': {'task': 'parse_news.celery_funcs.launch_spider',
                                                    'schedule': 60 * 60 + 10,
                                                    'args': ("snob.ru", "celery"),  #
                                                    },
                                'launch_techno-news_60m': {'task': 'parse_news.celery_funcs.launch_spider',
                                                           'schedule': 60 * 60 + 11,
                                                           'args': ("techno-news.ru", "celery"),  #
                                                           },
                                'launch_windozo_60m': {'task': 'parse_news.celery_funcs.launch_spider',
                                                       'schedule': 60 * 60 + 12,
                                                       'args': ("windozo.ru", "celery"),  #
                                                       },
                                'tokenize_ml_keywords_60m': {'task': 'tokenizer.tokenize_from_db.main',
                                                             'schedule': 60 * 60,
                                                             'args': ("temp_article",),
                                                             },
                                }
