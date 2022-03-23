#!/usr/bin/python3
""" Program that keep cleant the version folder of web static """
from datetime import datetime
from fabric.api import *
from os import path

env.hosts = ['34.75.163.65', '3.229.120.59']


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


def do_deploy(archive_path):
    """ Distributes an archive to the web servers """
    if not path.exists(archive_path):
        return False
    # split the path and get the second element in the list
    file_path = archive_path.split("/")[1]
    serv_folder = "/data/web_static/releases/" + file_path

    try:
        put(archive_path, "/tmp/")
        run("sudo mkdir -p " + serv_folder)
        run("sudo tar -xzf /tmp/" + file_path + " -C " + serv_folder + "/")
        run("sudo rm /tmp/" + file_path)
        run("sudo mv " + serv_folder + "/web_static/* " + serv_folder)
        run("sudo rm -rf " + serv_folder + "/web_static")
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s " + serv_folder + " /data/web_static/current")
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """ Call the do_pack() function and store the path of the created archive
    Call the do_deploy(archive_path) function, using the new
    path of the new archive
    Return False if no archive has been created
    Return the return value of do_deploy"""
    file_path = do_pack()
    if file_path is None:
        return False

    return (do_deploy(file_path))


def do_clean(number=0):
    """ Deletes out-of-date archives
    number is the number of the archives, including the most recent, to keep"""
    number = int(number)
    # keep only the most recent version of your archive
    if (number == 1 or number == 0):
        local('cd versions; ls -t | head -n -1 | xargs rm -rf')
        run('cd /data/web_static/releases; ls -t | head -n -1 | xargs rm -rf')
    else:
        local('cd versions; ls -t | head -n -{} | xargs rm -rf'.format(number))
        run('cd /data/web_static/releases; ls -t | head -n -{} | xargs rm -rf'.
            format(number))
