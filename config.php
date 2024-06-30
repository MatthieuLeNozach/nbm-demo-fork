<?php
$CONFIG = array (
  'htaccess.RewriteBase' => '/',
  'memcache.local' => '\\OC\\Memcache\\APCu',
  'apps_paths' => 
  array (
    0 => 
    array (
      'path' => '/var/www/html/apps',
      'url' => '/apps',
      'writable' => false,
    ),
    1 => 
    array (
      'path' => '/var/www/html/custom_apps',
      'url' => '/custom_apps',
      'writable' => true,
    ),
  ),
  'upgrade.disable-web' => true,
  'instanceid' => 'octwc8uy2vcc',
  'passwordsalt' => 'FS/jP4Ct/8MWzWrGE5BxqfxkDJsKbI',
  'secret' => 'WD9+TbEkGhVIoQxIcwMOfrwhZGnNpIpAehvKL0CD+ZC0Vwlh',
  'trusted_domains' => 
  array (
    0 => 'localhost:8080',
    1 => 'nextcloud',
    2 => 'localhost',
  ),
  'datadirectory' => '/var/www/html/data',
  'dbtype' => 'mysql',
  'version' => '29.0.3.4',
  'overwrite.cli.url' => 'http://localhost:8080',
  'dbname' => 'nextcloud',
  'dbhost' => 'dbnxt',
  'dbport' => '',
  'dbtableprefix' => 'oc_',
  'mysql.utf8mb4' => true,
  'dbuser' => 'nextcloud',
  'dbpassword' => 'root',
  'installed' => true,
);