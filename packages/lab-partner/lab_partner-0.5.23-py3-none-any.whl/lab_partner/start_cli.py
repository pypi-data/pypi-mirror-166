#!/usr/bin/env python

import subprocess
import os
import click
import sys

if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata


user = os.environ['USER']
home = os.environ['HOME']
display = os.environ['DISPLAY']


workspace = os.environ['WORKSPACE']
workspace_data = os.path.join(workspace, 'data')
network_name = 'lab'


def uid():
    rs = subprocess.run(['id', '-u'], capture_output=True)
    return rs.stdout.decode('utf-8').strip('\n')


def gid():
    rs = subprocess.run(['id', '-g'], capture_output=True)
    return rs.stdout.decode('utf-8').strip('\n')


def docker_gid():
    rs = subprocess.run(['getent', 'group', 'docker'], capture_output=True)
    full_group_info = rs.stdout.decode('utf-8').strip('\n')
    return full_group_info.split(':')[2]


def lab_partner_version():
    return metadata.version('lab-partner')


@click.command()
def start_cli():
    cmd = f'docker run -it --rm \
            -e USER={user} \
            -e UID={uid()} \
            -e GID={gid()} \
            -e DOCKER_GID={docker_gid()} \
            -e DISPLAY={display} \
            -e WORKSPACE={workspace} \
            -e WORKSPACE_DATA={workspace_data} \
            -e NETWORK_NAME={network_name} \
            -e LAB_PARTNER_VERSION={lab_partner_version()} \
            -v {home}/.docker:/opt/lab-partner/home/.docker \
            -v {home}/.gitconfig:/opt/lab-partner/home/.gitconfig \
            -v {home}/.pypirc:/opt/lab-partner/home/.pypirc \
            -v {workspace}:{workspace} \
            -v /var/run/docker.sock:/var/run/docker.sock \
            -w {workspace} \
            --network={network_name} \
            --privileged \
            enclarify/lab-partner-cli:{lab_partner_version()}'.split()
    os.execvp(cmd[0], cmd)


if __name__ == '__main__':
    start_cli()
