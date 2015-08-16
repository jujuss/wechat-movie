#! /usr/bin/env python
# -*- coding:utf-8 -*-
import os
from fabric.api import (
    local,
    lcd,
    settings,
)
from fabric.contrib.files import exists
from fabric.colors import (
    green,
    red,
)

SERVICES = ['wechat_movie']
MAIN_PIP_INDEX_URL = 'https://pypi.python.org/simple/'
DEPLOY_PARAMS = {
    'virtualenv': '/data/wechat-movie/venv',
    'remote_dir': '/data/wechat-movie/',
    'local_dir': os.path.dirname(os.path.realpath(__file__)),
}


def _init_virtualenv(virtualenv):
    local('sudo virtualenv {0}'.format(virtualenv))
    local('sudo {0}/bin/pip install -i {1} -U distribute pip'.format(
        virtualenv, MAIN_PIP_INDEX_URL
    ))


def _install_requirements(deployment_params):
    command = 'sudo {0}/bin/pip install -r requirements.txt -i {1}'.format(
        deployment_params['virtualenv'], MAIN_PIP_INDEX_URL
    )
    with lcd(deployment_params['remote_dir']):
        local(command)

def services_refresh(services):
    for service in services:
        with settings(warn_only=True):
            status = local('sudo supervisorctl status {0}'.format(service))
            if 'STOPPED' in status:
                continue
            local('sudo supervisorctl restart {0}'.format(service))

def status(services):
    for service in services:
        with settings(warn_only=True):
            status = local('sudo supervisorctl status {0}'.format(service))
            if 'STOPPED' in status:
                print(red(status))
            else:
                print(green(status))

def _transfer_files(local_dir, remote_dir):
    # local transfer
    if notos.path.exists(remote_dir):
        local('sudo cp {0} {1} -R'.format(local_dir, remote_dir))
    else:
        local('sudo cp {0}/* {1}/ -R'.format(local_dir, remote_dir))


def _do_depoly(deployment_params):
    if not os.path.exists(deployment_params['virtualenv']):
        _init_virtualenv(deployment_params['virtualenv'])
    _transfer_files(deployment_params['local_dir'],
                    deployment_params['remote_dir'])
    _install_requirements(deployment_params)


def deploy():
    for service in SERVICES:
        print(green('deploy %s' % service))
        _do_depoly(DEPLOY_PARAMS)
    services_refresh(SERVICES)
    status(SERVICES)
