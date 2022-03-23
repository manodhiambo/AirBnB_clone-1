# Manifest that configures a web server for deployment
exec { 'exec_0':
  command => 'sudo sudo apt-get update -y',
  path    => ['/usr/bin', '/bin'],
  returns => [0,1]
}

exec { 'exec_1':
  require => Exec['exec_0'],
  command => 'sudo apt-get install nginx -y',
  path    => ['/usr/bin', '/bin'],
  returns => [0,1]
}

exec { 'exec_2':
  require => Exec['exec_1'],
  command => 'sudo mkdir -p /data/web_static/shared/',
  path    => ['/usr/bin', '/bin'],
  returns => [0,1]
}

exec { 'exec_3':
  require => Exec['exec_2'],
  command => 'sudo mkdir -p /data/web_static/releases/test/',
  path    => ['/usr/bin', '/bin'],
  returns => [0,1]
}

exec { 'exec_4':
  require => Exec['exec_3'],
  command => 'sudo touch /data/web_static/releases/test/index.html',
  path    => ['/usr/bin', '/bin'],
  returns => [0,1]
}

exec { 'exec_5':
  require => Exec['exec_4'],
  command => 'echo "Holberton School" | sudo tee /data/web_static/releases/test/index.html >/dev/null',
  path    => ['/usr/bin', '/bin'],
  returns => [0,1]
}

exec { 'exec_6':
  require => Exec['exec_5'],
  command => 'rm -rf /data/web_static/current',
  path    => ['/usr/bin', '/bin', '/usr/sbin'],
  returns => [0,1]
}


exec { 'exec_7':
  require => Exec['exec_6'],
  command => 'sudo ln -sf /data/web_static/releases/test/ /data/web_static/current',
  path    => ['/usr/bin', '/bin', '/usr/sbin'],
  returns => [0,1]
}

exec { 'exec_8':
  require => Exec['exec_7'],
  command => 'sudo chown -R ubuntu:ubuntu /data/',
  path    => ['/usr/bin', '/bin', '/usr/sbin'],
  returns => [0,1]
}

exec { 'exec_9':
  require     => Exec['exec_8'],
  environment => ['C=\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}\n'],
  command     => 'sudo sed -i "38i $C" /etc/nginx/sites-available/default',
  path        => ['/usr/bin', '/bin'],
  returns     => [0,1]
}

exec { 'exec_10':
  require => Exec['exec_9'],
  command => 'sudo service nginx restart',
  path    => ['/usr/bin', '/bin', '/usr/sbin'],
  returns => [0,1]
}
