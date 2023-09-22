#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy
"""

from fabric.api import *
import os


env.hosts = ['100.25.170.22' '35.174.185.161']


def do_deploy(archive_path):
    """Deploy an archive to the web servers"""
    try:
        try:
            if os.path.exists(archive_path):
                # Extract archive to the /data/web_static/releases/
                arc_tgz = archive_path.split("/")
                arg_save = arc_tgz[1]
                arc_tgz = arc_tgz[1].split(".")
                arc_tgz = arc_tgz[0]

                # Upload archive to the server
                put(archive_path, "/tmp")

                # save folder paths in variables
                uncomp_fold = "/data/web_static/releases/{}".format(arc_tgz)
                tmp_location = "/tmp/{}".format(arg_save)

                # Run remote commands on the server
                run("mkdir -p {}".format(uncomp_fold))
                run("tar -xzf /tmp/{} -C {}".format(tmp_location, uncomp_fold))

                # Delete the archive from the web server
                run("mv {}/web_static/* {}".format(uncomp_fold, uncomp_fold))
                run("rm -rf {}/web_static".format(uncomp_fold))
                run("rm -rf /data/web_static/current")
                run("ln -sf {} /data/web_static/current".format(uncomp_fold))
                run("sudo service nginx restart")
                return True
            else:
                print("File does not exist")
                return False
        except Exception as err:
            print(err)
            return False

    except Exception:
        print("error")
        return False
