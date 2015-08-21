import os
from contextlib import contextmanager as _contextmanager

from fabric.api import prefix, local, cd, run, put, env
from fabric.colors import red, green
from getenv import env as getenv

from settings import THEME_DIR, THEME_STATIC_DIR, PROJECT_ROOT, ENV_ROOT


deployments = {
    'live': {
        "host": getenv('DEPLOYMENT_HOST_LIVE'),
        "port": getenv('DEPLOYMENT_PORT_LIVE'),
        "user": getenv('DEPLOYMENT_USER_LIVE'),
        "path": getenv('DEPLOYMENT_PATH_LIVE'),
        "venv": getenv('DEPLOYMENT_VENV_PATH_LIVE'),
    }
}
default_deployment = 'live'

@_contextmanager
def virtualenv(context):
    if context not in deployments.keys():
        yield
        return
    with prefix('source ' + deployments[context]["venv"] + '/bin/activate'):
        yield


def deploy(context=default_deployment, static=False):
    dep = deployments[context]
    env.host_string = dep["host"]+':'+str(dep["port"])
    env.user = dep["user"]
    deploy_path = dep["path"]

    if context != 'live':
        print(green(context.upper() + ' deploy'))
    else:
        print(red("LIVE DEPLOY WITH STATIC" if static else "LIVE DEPLOY"))

    if static:
        print("rebuilding static files included")

    if static:
        local(os.path.join(THEME_DIR, 'build.sh'))

    with virtualenv(context):
        with cd(deploy_path):
            run('git pull')
            if static:
                with cd(THEME_DIR.replace(PROJECT_ROOT, deploy_path.rstrip('/')+'/')):
                    run('git pull')
                put(THEME_STATIC_DIR, './'+THEME_STATIC_DIR.replace(PROJECT_ROOT, '').lstrip('/'))
                run('./manage.py collectstatic --noinput')
            # run('./manage.py compilemessages -l bg')
            run('./manage.py migrate')
            run('touch ' + os.path.join(ENV_ROOT.replace(PROJECT_ROOT, ''), 'wsgi.py'))
