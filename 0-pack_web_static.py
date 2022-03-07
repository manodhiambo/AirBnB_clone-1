#!/usr/bin/python3
""" Program that compress a dir with tar before sending """
from datetime import datetime
from fabric.api import *


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
