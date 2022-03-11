### Development with Docker Toolbox

If you are using **Docker Toolbox** in Windows or macOS instead of **Docker for Windows** or **Docker for Mac**, Docker will be running in a VirtualBox Virtual Machine, and it will have a local IP different than `127.0.0.1`, which is the IP address for `localhost` in your machine.

The address of your Docker Toolbox virtual machine would probably be `192.168.99.100` (that is the default).

As this is a common case, the domain `local.dockertoolbox.tiangolo.com` points to that (private) IP, just to help with development (actually `dockertoolbox.tiangolo.com` and all its subdomains point to that IP). That way, you can start the stack in Docker Toolbox, and use that domain for development. You will be able to open that URL in Chrome and it will communicate with your local Docker Toolbox directly as if it was a cloud server, including CORS (Cross Origin Resource Sharing).

If you used the default CORS enabled domains while generating the project, `local.dockertoolbox.tiangolo.com` was configured to be allowed. If you didn't, you will need to add it to the list in the variable `BACKEND_CORS_ORIGINS` in the `.env` file.

To configure it in your stack, follow the section **Change the development "domain"** below, using the domain `local.dockertoolbox.tiangolo.com`.

After performing those steps you should be able to open: http://local.dockertoolbox.tiangolo.com and it will be server by your stack in your Docker Toolbox virtual machine.

Check all the corresponding available URLs in the section at the end.

### Development with Docker Toolbox URLs

Development URLs, for local development.

Frontend: http://local.dockertoolbox.tiangolo.com

Backend: http://local.dockertoolbox.tiangolo.com/api/

Automatic Interactive Docs (Swagger UI): https://local.dockertoolbox.tiangolo.com/docs

Automatic Alternative Docs (ReDoc): https://local.dockertoolbox.tiangolo.com/redoc

PGAdmin: http://local.dockertoolbox.tiangolo.com:5050

Flower: http://local.dockertoolbox.tiangolo.com:5555

Traefik UI: http://local.dockertoolbox.tiangolo.com:8090
