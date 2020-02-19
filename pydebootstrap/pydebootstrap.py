#!/usr/bin/python3 -B

import subprocess
import os
import shutil
import sys
from . import config


def create(conf):
    """ Check for the debootstrap command and create a debian based jail from source.
        Requires:
            conf:
              components:   <comma separated list of repos to add>
              includes:     <comma separated list of packages to install
              arch:         architecture (currently supported amd64)
              os:           <debian based operating system flavor>
              source:       <URL to fetch the operating system files from>
              name:         <machine name>
    """
    try:
        bootstrap_cmd_check = subprocess.run(['which', 'debootstrap'], stdout=subprocess.PIPE)
        bootstrap_cmd_check.check_returncode()
        bootstrap_cmd = bootstrap_cmd_check.stdout.decode('utf8').strip('\n')
    except subprocess.CalledProcessError as e:
        print(e)
    
    debootstrap_nonos = [ 'os', 'id', 'source', 'arch', 'commands']
    debootstrap_args_list = [ ['--' + key, conf[key]] for key in conf.keys() if key not in debootstrap_nonos and conf[key] is not None ]
    debootstrap_args = [ arg for args_pair in debootstrap_args_list for arg in args_pair ]
    positional = ['--arch', conf['arch'], conf['os'], config.jailhouse + conf['id'], conf['source']]
    debootstrap = [ bootstrap_cmd ]
    debootstrap.extend(debootstrap_args)
    debootstrap.extend(positional)
    try:
        subprocess.check_call(debootstrap)
    except subprocess.CalledProcessError as e:
        print(e)


def release(name):
    """ machinectl terminate the environment if it exists, and remove the debootstrapped directory"""
    s1 = subprocess.Popen(['systemctl'], stdout=subprocess.PIPE)
    data, err = s1.communicate()
    services = data.decode('utf8').replace(" ","").split('\n')
    result = [ x for x in services if name in x ]
    if not result:
        print("No systemd services found")
    else:
        print("Services found. Terminating...")
        with open(os.devnull, 'w') as FNULL:
            try:
                subprocess.check_call(['machinectl', 'terminate', name], stdout=FNULL, stderr=FNULL)
            except subprocess.CalledProcessError as e:
                    for service in result: subprocess.call(['systemctl', 'kill', service])
                    subprocess.call(['systemctl', 'reset-failed'])

    if os.path.isdir(config.jailhouse + name):
        shutil.rmtree(config.jailhouse + name)
    else:
        print("No jail by that name in the jailhouse")


def list():
    try:
        roster_check = subprocess.run(['ls', config.jailhouse], stdout=subprocess.PIPE)
        roster_check.check_returncode()
        roster = roster_check.stdout.decode('utf8')
    except subprocess.CalledProcessError as e:
        print(e)

    print(roster)
