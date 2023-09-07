#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static

echo -e "\e[1;32m START\e[0m"

# Install nginx
sudo apt-get -y update
sudo apt-get install -y nginx

echo -e "\e[1;32m Packages updated\e[0m"
echo

# firewall configuration
sudo ufw allow 'Nginx HTTP'
echo -e "\e[1;32m Allow incoming NGINX HTTP connections\e[0m"
echo

# create the required directories
sudo mkdir -p /data/web_static/shared
sudo mkdir -p /data/web_static/releases/test
echo -e "\e[1;32m directories created"
echo

# fake html file to test nginx configuration
echo "<h1>Welcome to www.allmilly.tech</h1>" > /data/web_static/releases/test/index.html
echo -e "\e[1;32m Test string added\e[0m"
echo

# prevent overwriting
if [ -d "/data/web_static/current" ];
then
	echo "path /data/web_static/current exists"
	sudo rm -rf /data/web_static/current;
fi;
echo -e "\e[1;32m prevent overwriting\e[0m"
echo

# create a symbolic link
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# set permissions
sudo chown -R ubuntu:ubuntu /data

# Update Nginx configuration
sudo sed -i '38i\\tlocation /hbnb_static/ {\n\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

sudo ln -sf '/etc/nginx/sites-available/default' '/etc/nginx/sites-available/default'
echo -e "\e[1;32m Symbolic link created\e[0m"
echo

# restart nginx
sudo service nginx restart
echo -e "\e[1;32m restart NGINX\e[0m"
