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

Press `a` to insert <br>
Change the array `'trusted_domains'` by adding `1 => 'nextcloud', ` <br>
Press `echap` <br>
Press `:` <br>
Press `x` <br>
Press `Enter` to validate <br>
