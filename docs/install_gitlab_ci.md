# Install CI/CD for NBM Platform

https://docs.gitlab.com/runner/install/linux-manually.html

### Download gitlab-runner

```bash
curl -LJO "https://gitlab-runner-downloads.s3.amazonaws.com/latest/deb/gitlab-runner_amd64.deb"

sudo dpkg -i gitlab-runner_amd64.deb
```

### Après ça on a le bot

gitlab-runner pour tester

### Ajouter gitlab runner au group docker

```bash
sudo groupadd docker

sudo usermod -aG docker gitlab-runner
```

Pour tester
sudo su - gitlab runner
docker ps

Pour enregistre run runner

https://gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration/-/settings/ci_cd

sudo gitlab-runner register
URL
https://gitlab.com/
Registration token
Autogenerate voir catpure d'écran envoyée à Javi le 26 mars
Description
nbm
Tag
nbm
Executor
shell

gitlab-runner start pour executer le runner

On va faire un fichier pour les étapes du processsus
.gitlab-ci.yml

A chaque modification de ce fichier on doit pousser

Pbmatique on avait l'erreur
https://gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration/-/jobs/1130804606
due à la onfiguration debian ubuntu
Par défaut il ajoute un fichier .bash_logout qui une fois qu'il a finit de faire sa session il va détruire la console mais si on fait ça dans gitlab on ne verrait pas le résultat donc on doit commenter les lignes :

Pour le faire on doit faire sudo su - gitlab-runner

vim .bash_logout

```bash
#if [ "$SHLVL" = 1 ]; then
#    [ -x /usr/bin/clear_console ] && /usr/bin/clear_console -q
#fi
```

D'abord on va tester de faire un deployment
On va builder les images

Déploiment, configuration serveur

Dans opt on va créer un dossier nbm

```bash
sudo mkdir nbm
```

Propriétaire du dossier nbm gitlab-runner

sudo chown gitlab-runner:gitlab-runner nbm
