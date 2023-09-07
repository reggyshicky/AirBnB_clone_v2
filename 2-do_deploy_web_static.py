#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy
"""

from fabric.api import *
import os


env.hosts = ['100.25.170.22' '35.174.185.161']
env.user = 'ubuntu'


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
