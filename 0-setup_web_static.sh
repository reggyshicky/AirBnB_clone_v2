#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static

# Check if Nginx is installed
if ! [ -x "$(command bginx -v)" ]; then
	sudo apt-get update
	sudo apt-get install -y nginx
fi

# start nginx
sudo service nginx start

# firewall configuration
sudo ufw allow 'Nginx HTTP'

# create the required directories
sudo mkdir -p /data/web_static/shared
sudo mkdir -p /data/wev_static/releases/test

# fake html file to test nginx configuration
echo "<h1>Welcome to www.allmilly.tech</h1>" > /data/web_static/releases/test/index.html

# prevent file overwriting
if [ -d "/data/web_static/current" ];
then
    echo "path /data/web_static/current exists"
    sudo rm -rf /data/web_static/current;
fi;

# create a symbolic link
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# set permissions
sudo chown -hR ubuntu:ubuntu /data

# Update Nginx configuration
sudo sed -i '38i\\tlocation /hbnb_static/ {\n\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

# restart nginx
sudo service nginx restart
