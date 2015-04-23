from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/ujuc/django_tdd.git'

def deploy():
    site_folder = '/home/{0}/sites/{1}'.format(env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_datebase(source_folder)

def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('daabase', 'static', 'virtualenv', 'source'):
        run('mkdir -p {0}/{1}'.format(site_folder, subfolder))

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd {0} && git fetch'.format(source_folder))
    else:
        run('git clone {0} {1}'.format(REPO_URL, source_folder))

    current_commit = local("git log -1 --format=%H", capture=True)
    run('cd {0} && git rest --hard {1}'.format(source_folder, current_commit))

def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS = .+$',
        'ALLOWED_HOSTS = ["{1}"]'.format(site_name)
    )
    secret_key_file = source_folder + '/superlists/secret_key_file.py'
    if not exists(secret_key_file):
        chars = 'abcdefghihklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s" % (key))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder))
    run('%s/bin/pip install -r %s/requirements.txt' % (
        virtualenv_folder, source_folder
    ))

def _update_static_files(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % (source_folder))

def _update_datebase(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (
        source_folder
    ))
