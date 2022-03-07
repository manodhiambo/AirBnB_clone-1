#!/usr/bin/python3
""" Program that distributes an archive to your web servers,
cusing the function do_deploy """
from datetime import datetime
from fabric.api import *
from os import path

env.hosts = ['35.243.214.144', '34.233.133.27']


def do_pack():
    """ Generates a .tgz archive from the contents of the web_static
    folder of your AirBnB Clone repo """
    date_str = datetime.now().strftime('%Y%m%d%H%M%S')
    local("mkdir -p versions/")
    try:
        local("tar -cvzf versions/web_static_{}.tgz web_static"
              .format(date_str))
        return "versions/web_static_{}.tgz".format(date_str)
    except Exception:
        return None

