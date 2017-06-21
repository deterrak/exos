# EXOS

EXOS is a small pack written for Brocade Workflow compser and the Extreme Network EXOS operating system. The pack is designed to provide remote access to the Extreme Networks EXOS devices.

This pack allows you to define commands to be run on the switch. The commands are defined in a text file which you can reference in your workflow.

The Following variables can be use within your work flow
  - Login username
  - Login username's password
  - Switch IP address
  - File that defines the commands that will be executed on the switch

### Tech
EXOS requires:
* Workflow Composer
* Pexpect - a python expect module

### Installation

EXOS requires pexpect to run.
Install the dependencies and devDependencies and start the server.


cd /opt/stackstorm/packs/EXOS

```sh
$ Get EXOS from github (https://github.com/deterrak/exos) 
$ sudo st2 run packs.setup_virtualenv packs=EXOS
$ sudo st2ctl reload
```
Refresh the Workflow Composer web page and the EXOS package will appear on the Actions tab.

License
----
EXOS is released under the APACHE 2.0 license.
