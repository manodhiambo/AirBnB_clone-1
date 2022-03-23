# Puppet for setup, Redo the task #0
exec { 'Update Packages':
  command  => 'sudo apt-get update -y',
  provider => shell
}
exec { 'Install Nginx':
  command  => 'sudo apt-get install nginx -y',
  provider => shell,
  require  => Exec['Update Packages']
}
exec { 'Create Shared Folder':
  command  => 'sudo mkdir -p /data/web_static/shared/',
  provider => shell,
  require  => Exec['Install Nginx']
}
exec { 'Create Test Folder':
  command  => 'sudo mkdir -p /data/web_static/releases/test/',
  provider => shell,
  require  => Exec['Create Shared Folder']
}
exec { 'Create Fake File':
  command  => 'echo "Holberton School" > /data/web_static/releases/test/index.html',
  provider => shell,
  require  => Exec['Create Test Folder'],
  returns  => [0, 1]
}
exec { 'Symbolic Link':
  command  => 'sudo ln -sf /data/web_static/releases/test/ /data/web_static/current',
  provider => shell,
  require  => Exec['Create Fake File']
}
exec { 'Give Ownership':
  command  => 'sudo chown -R ubuntu:ubuntu /data/',
  provider => shell,
  require  => Exec['Symbolic Link']
}
exec { 'Add Location':
  command  => 'sudo sed -i "38i\\\n\tlocation \/hbnb_static\/ {\n\t\talias \/data\/web_static\/current\/;\n\t}\n" /etc/nginx/sites-enabled/default',
  provider => shell,
  require  => Exec['Give Ownership']
}
exec { 'Reload Nginx':
  command  => 'sudo service nginx reload',
  provider => shell,
  require  => Exec['Add Location']

}
exec { 'Restart Nginx':
  command  => 'sudo service nginx restart',
  provider => shell,
  require  => Exec['Reload Nginx']
}
