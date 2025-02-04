#! /usr/bin/env sh

# Exit in case of error
set -e

DOMAIN=backend \
SMTP_HOST="" \
TRAEFIK_PUBLIC_NETWORK_IS_EXTERNAL=false \
INSTALL_DEV=true \
docker-compose -p tests \
-f docker-compose.yml \
config > docker-stack.yml

docker-compose -p tests -f docker-stack.yml build --build-arg app_user=nbm
docker-compose -p tests -f docker-stack.yml down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
docker-compose -p tests -f docker-stack.yml up -d
sleep 60
docker-compose -p tests -f docker-stack.yml exec -T backend bash /app/tests-start.sh "$@"
docker-compose -p tests -f docker-stack.yml down -v --remove-orphans
