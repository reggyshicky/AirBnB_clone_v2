#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy
"""

from fabric.api import *
from datetime import datetime
import os


env.hosts = ['100.25.170.22' '35.174.185.161']
env.user = 'ubuntu'


def do_pack():
    """Creates a compressed archive"""
    if not os.path.exists("versions"):
        local("mkdir versions")
    now = datetime.now()
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour,
            now.minute, now.second)
    print("Packing web_static to versions/{}".format(archive_name))
    command = "tar -cvzf versions/{} web_static".format(archive_name)
    res = local(command)

    file_size = os.path.getsize("versions/{}".format(archive_name))
    print("web_static packed: versions/{} -> {}Bytes".format(
        archive_name, file_size))
    if res.succeeded:
        return "versions/{}".format(archive_name)
    else:
        return None


def do_deploy(archive_path):
    """Deploy an archive to the web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ dir in the webserver
        put(archive_path, "/tmp/")

        # Extract archive to the /data/web_static/releases/
        filename = archive_path.split("/")[-1]
        direc = "/data/web_static/releases/{}".format(
            filename.split(".")[0])
        run("sudo mkdir -p {}".format(direc))
        run("sudo tar -xzf /tmp/{} -C {} --strip-components=1".format(
            filename, direc))

        # Delete the archive from the web server
        run("sudo rm /tmp/{}".format(filename))

        # Delete symbolic link /data/web_static/current on web server
        run("sudo rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current on web server
        run("sudo ln -s {} /data/web_static/current".format(direc))

        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """Interface for set-up"""
    archive_path = do_pack()

    if archive_path is None:
        return False
    res = do_deploy(archive_path)
    return res
