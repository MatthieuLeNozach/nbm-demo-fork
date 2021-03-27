
### Live development with Python Jupyter Notebooks

If you know about Python [Jupyter Notebooks](http://jupyter.org/), you can take advantage of them during local development.

The `docker-compose.override.yml` file sends a variable `env` with a value `dev` to the build process of the Docker image (during local development) and the `Dockerfile` has steps to then install and configure Jupyter inside your Docker container.

So, you can enter into the running Docker container:

```bash
docker-compose exec backend bash
```

And use the environment variable `$JUPYTER` to run a Jupyter Notebook with everything configured to listen on the public port (so that you can use it from your browser).

It will output something like:

```console
root@73e0ec1f1ae6:/app# $JUPYTER
[I 12:02:09.975 NotebookApp] Writing notebook server cookie secret to /root/.local/share/jupyter/runtime/notebook_cookie_secret
[I 12:02:10.317 NotebookApp] Serving notebooks from local directory: /app
[I 12:02:10.317 NotebookApp] The Jupyter Notebook is running at:
[I 12:02:10.317 NotebookApp] http://(73e0ec1f1ae6 or 127.0.0.1):8888/?token=f20939a41524d021fbfc62b31be8ea4dd9232913476f4397
[I 12:02:10.317 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[W 12:02:10.317 NotebookApp] No web browser found: could not locate runnable browser.
[C 12:02:10.317 NotebookApp]

    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://(73e0ec1f1ae6 or 127.0.0.1):8888/?token=f20939a41524d021fbfc62b31be8ea4dd9232913476f4397
```

you can copy that URL and modify the "host" to be `localhost` or the domain you are using for development (e.g. `local.dockertoolbox.tiangolo.com`), in the case above, it would be, e.g.:

```
http://localhost:8888/token=f20939a41524d021fbfc62b31be8ea4dd9232913476f4397
```

and then open it in your browser.

You will have a full Jupyter Notebook running inside your container that has direct access to your database by the container name (`db`), etc. So, you can just run sections of your backend code directly, for example with [VS Code Python Jupyter Interactive Window](https://code.visualstudio.com/docs/python/jupyter-support-py) or [Hydrogen](https://github.com/nteract/hydrogen).
