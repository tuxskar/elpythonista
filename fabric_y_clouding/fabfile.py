import posixpath
from contextlib import contextmanager

from fabric.context_managers import cd, prefix, warn_only
from fabric.operations import run
from fabric.state import env
from fabric.api import sudo, local, task

env.hosts = ['85.208.23.73']
env.user = "root"
env.VENV_PATH = 'venv'
env.APP_PATH = '/root/django_a_fondo'
env.password = 'k2sC8frNDsmeyqfb'

app_name = 'daf'


@task
def uptime():
    run('uptime')


@task
def restart_nginx():
    sudo('systemctl restart nginx')


@task
def super_status():
    run(f'supervisorctl status')


@contextmanager
def virtualenv():
    with prefix("source %s" % posixpath.join(env.VENV_PATH, "bin/activate")):
        yield


@contextmanager
def access_app():
    with cd(env.APP_PATH):
        yield


PACKAGE_LIST = ['git', 'supervisor', 'nginx',
                'python3.8-venv']  # add all required packages in this list


def install_package():
    sudo('apt-get update')
    sudo('apt-get install %s' % (' '.join(PACKAGE_LIST)))


def update_code():
    # run('git pull')
    pass


@task
def app_status():
    run(f'supervisorctl status {app_name}')


def create_virtualenv():
    run('python3 -m venv venv')


def restart_supervisor():
    sudo(f'supervisorctl restart {app_name}')


def deploy_django():
    run('pip install -r requirements.txt')
    run('python manage.py migrate')
    run('python manage.py collectstatic')


def add_fixtures():
    run('python manage.py loaddata blog_app/fixtures/*')


def setup_code():
    with warn_only():
        run("git clone https://github.com/Marcombo/python-a-fondo.git")
    run("cp -r python-a-fondo/Capitulo_10/django_a_fondo/ django_a_fondo")


def setup_services():
    with cd("/tmp"):
        with warn_only():
            run("rm -r elpythonista")
            run("git clone https://github.com/tuxskar/elpythonista.git")

        with cd("/tmp/elpythonista/fabric_y_clouding"):
            run('cp settings.py /root/django_a_fondo/django_a_fondo/settings.py')

            run('cp supervisor.conf /etc/supervisor/conf.d/daf.conf')
            run('systemctl restart supervisor')

            sudo('cp daf_nginx.conf /etc/nginx/sites-enabled/default')
            sudo('systemctl restart nginx')


@task
def setup():
    install_package()
    setup_code()
    with access_app():
        create_virtualenv()
        with virtualenv():
            deploy_django()
            add_fixtures()
    setup_services()


@task
def deploy():
    with access_app(), virtualenv():
        update_code()
        deploy_django()
    restart_supervisor()
