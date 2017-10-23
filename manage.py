from django.core.management import execute_from_command_line
import os
import sys
# from set_environment import DeployEnv
# from temp_config.set_environment import DeployEnv


#this needs to be added so that the stting in the subdirectory django app can be found
root_path = os.path.abspath(os.path.split(__file__)[0])
print('root path = {root_path}')
sys.path.insert(0, os.path.join(root_path, 'splash_app'))
sys.path.insert(0, root_path)

if __name__ == "__main__":

	print('manage.py')

	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_docker")
	# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_apache")
	print(sys.argv)
	# wsgi needs to know about where the settings file is
	execute_from_command_line(sys.argv)