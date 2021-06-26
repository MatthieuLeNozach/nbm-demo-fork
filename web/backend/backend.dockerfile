FROM registry.gitlab.com/nbm.challenge/nbm-nocturnal-bird-migration:backend-base

ARG app_user=nbm
USER ${app_user}

COPY --chown=${app_user} ./app ./
ENV PYTHONPATH=/app
