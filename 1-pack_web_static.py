#!/usr/bin/python3
"""Fabric script that generates a .tgz archive"""

from fabric.api import local
from datetime import datetime
from fabric.decorators import runs_once


@runs_once
def do_pack():
    """function that compresses a directory"""

    # Create an archive
    local('mkdir -p versions/')
    archive_path = ("versions/web_static_{}.tgz"
                    .format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")))
    res = local("tar -cvzf {} web_static/".format(archive_path))

    # Check if the archive was created successfully
    if res.succeeded:
        return archive_path
    return None
