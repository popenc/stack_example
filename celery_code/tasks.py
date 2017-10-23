"""
CTS celery instance
"""
from __future__ import absolute_import
import os
from os.path import dirname, abspath
import sys
from celery import Celery
import logging
import redis
import json


logging.getLogger('celery.task.default').setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)


# This is where the above should be removed, and instead
# the set_environment.py module could be ran to set env vars
# from the config/ env vars files.
# BUT, can the module be accessed from the parent dir???
# from qed_cts.set_environment import DeployEnv
# from temp_config.set_environment import DeployEnv
# runtime_env = DeployEnv()
# runtime_env.load_deployment_environment()


# from django.conf import settings
# settings.configure()
# if not os.environ.get('DJANGO_SETTINGS_FILE'):
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qed_cts.settings_outside')
# else:
#     # os.environ.setdefault('DJANGO_SETTINGS_MODULE', '.' + os.environ.get('DJANGO_SETTINGS_FILE'))
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

redis_hostname = os.environ.get('REDIS_HOSTNAME')
redis_port = os.environ.get('REDIS_PORT')
REDIS_HOSTNAME = os.environ.get('REDIS_HOSTNAME')

if not os.environ.get('REDIS_HOSTNAME'):
    os.environ.setdefault('REDIS_HOSTNAME', 'localhost')
    REDIS_HOSTNAME = os.environ.get('REDIS_HOSTNAME')

logging.info("REDIS HOSTNAME: {}".format(REDIS_HOSTNAME))

redis_conn = redis.StrictRedis(host=REDIS_HOSTNAME, port=6379, db=0)  # hostname=redis for docker

# redis_conn = redis.StrictRedis(host=REDIS_HOSTNAME, port=6379, db=0)

app = Celery('tasks',
				broker='redis://{}:6379/0'.format(REDIS_HOSTNAME),	
				backend='redis://{}:6379/0'.format(REDIS_HOSTNAME))

app.conf.update(
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
)



##### THE TASKS #####

@app.task
def test_celery(sessionid, message):
    logging.info("celery app received message: {}".format(message))
    logging.info("returning message 'hello from celery' to nodejs..")
    redis_conn.publish(sessionid, "hello from celery")  # async push to user