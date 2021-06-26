FROM registry.gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration:celeryworker-base

ARG app_user=nbm
USER ${app_user}

COPY --chown=${app_user}  ./app/worker-start.sh ./worker-start.sh

RUN chmod +x ./worker-start.sh

CMD ["bash", "./worker-start.sh"]
