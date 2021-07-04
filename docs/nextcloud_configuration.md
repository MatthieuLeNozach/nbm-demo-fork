### To configure your nextcloud 

Go to localhost:8080

Enter choosen USER and PASSWORD (default "test" for both) that you set also in .env file with :

```console
NEXTCLOUD_HOST="http://nextcloud"
NEXTCLOUD_USER="USER"
NEXTCLOUD_PASSWORD="PASSWORD"
````

Create `/mediae/audio` folder in nextcloud interface 

Run sh 

```console
docker-compose exec nextcloud sh
````
Install VIM

```console
apt-get update
apt-get install vim
````
Edit config/config.php file

```console
vim config/config.php
````
Set array of trusted domains 

```console
Press `a` to insert 
Change the array 'trusted_domains' by adding 1 => 'nextcloud', 
Press `echap` 
Press `:` 
Press `x` 
Press `Enter` to validate 
````
