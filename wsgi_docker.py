"""
WSGI config for UberDjango project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application
# from temp_config.set_environment import DeployEnv
# from qed_cts.temp_config.set_environment import DeployEnv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_docker")

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_docker")

application = get_wsgi_application()
