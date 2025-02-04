FROM node:alpine

# Create app directory
RUN mkdir -p /usr/app
WORKDIR /usr/app

# Installing dependencies
COPY package*.json /

# Install python and vips-dev for dotenv (for sharp (for node-gyp))
RUN apk add --update --no-cache --repository http://dl-3.alpinelinux.org/alpine/edge/community \
        --repository http://dl-3.alpinelinux.org/alpine/edge/main vips-dev &&\
    apk add --no-cache --virtual .gyp \
        python3 make g++

RUN npm install