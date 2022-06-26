# Pydebootstrap

## Description

Python debootstrap wrapper. Creates and manages chroot environments in a systemd-machined compatible way.
Users running this script must have r/w access to /var/lib/machines.


## Functions

#### Create
pydebootstrap.create() requires a configuration profile like this one:

```
conf:
  id: 'Ubuntu1804'
  os: 'bionic'
  source: 'http://archive.ubuntu.com/ubuntu'
  arch: 'amd64'
  include: 'build-essential,python3,curl,wget,systemd,git,net-tools,systemd-sysv,dbus,vim'
  exclude: 
  components: 'main,universe'
  no-resolve-deps: 
  variant: 'buildd'
  keyring:
  foreign: 
  second-stage: 
  second-stage-target:
```

In the above example, an Ubuntu 1804 instance will be created in /var/lib/machines named Ubuntu1804.
The machine that the profile describes does not have to match the OS of the Parent Machine.

In the profile conf, any values left blank are omitted from the command, the config should be expandable to
support most if not all debootstrap arguments.

#### Release and List

pydebootstrap.release() requires only the name of the virtual machine that you wish to terminate

pydebootstrap.list() will print the names of each of the directories in /var/lib/mahines
