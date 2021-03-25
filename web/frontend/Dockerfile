# Base on offical Node.js Alpine image
FROM node:alpine

# Set working directory
WORKDIR /usr/app

# Install PM2 globally
RUN npm install --global pm2

# Copy package.json and package-lock.json before other files
# Utilise Docker cache to save re-installing dependencies if unchanged
COPY ./package*.json ./

# Install python and vips-dev for dotenv (for sharp (for node-gyp))
RUN apk add --update --no-cache --repository http://dl-3.alpinelinux.org/alpine/edge/community \
        --repository http://dl-3.alpinelinux.org/alpine/edge/main vips-dev &&\
    apk add --no-cache --virtual .gyp \
        python make g++

# Install dependencies
RUN npm install 
# RUN npm install --production

# Copy all files
COPY ./ ./

# Build app
RUN npm run build

# Expose the listening port
EXPOSE 3000

# Run container as non-root (unprivileged) user
# The node user is provided in the Node.js Alpine base image
USER node

# Run npm start script with PM2 when container starts
CMD [ "pm2-runtime", "npm", "--", "start" ]
