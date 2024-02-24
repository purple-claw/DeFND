DefNd
======

A Python firewall: Because slow networks are much secure networks.


Installation
------------

This section assumes that you are installing this program on Ubuntu 14.04 LTS.
This firewall should work on other Linux systems, but safety not guaranteed.

First, install the required packages. On Ubuntu, these are `iptables`, `python`,
`python-pip`, `build-essential`, `python-dev`, and
`libnetfilter-queue-dev`. Next, use `pip2` to install the project dependencies,
which can be found in `requirements.txt`.

The commands for both these operations are:

    sudo apt-get install python python-pip iptables build-essential python-dev libnetfilter-queue-dev
    pip install --user -r requirements.txt


Running
-------

The main file is `main.py`, which needs to be run as root to modify IPTables.
Additionally, main needs to receive a JSON configuration file as its first
argument. If running with the example configuration, the command is:

`sudo python2 main.py examples/example.json`

To stop DEFND, press Control-C.


Troubleshooting
---------------

Defnd should undo its changes to IPTables after exiting. However, if you are
unable to access the internet after exiting PyWall, view existing
IPTables rules with `sudo iptables -nL`. If a rule with the target chain
`NFQueue` lingers, delete it with
`sudo iptables -D INPUT -j NFQUEUE --queue-num [undesired-queue-number]`.

For INPUT rules, the command is `sudo iptables -D INPUT -j NFQUEUE --queue-num 1`.
For OUTPUT rules, the command is `sudo iptables -D OUTPUT -j NFQUEUE --queue-num 2`.

In case Defnd gives a message that another application has the xtables lock,
Control-C the server, ensure that all the IPTables rules are cleared, and
restart Defnd.