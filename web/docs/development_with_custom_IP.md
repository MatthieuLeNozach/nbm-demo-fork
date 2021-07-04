### Development with a custom IP

If you are running Docker in an IP address different than `127.0.0.1` (`localhost`) and `192.168.99.100` (the default of Docker Toolbox), you will need to perform some additional steps. That will be the case if you are running a custom Virtual Machine, a secondary Docker Toolbox or your Docker is located in a different machine in your network.

In that case, you will need to use a fake local domain (`dev.nocturnal-bird-migration.org`) and make your computer think that the domain is is served by the custom IP (e.g. `192.168.99.150`).

If you used the default CORS enabled domains, `dev.nocturnal-bird-migration.org` was configured to be allowed. If you want a custom one, you need to add it to the list in the variable `BACKEND_CORS_ORIGINS` in the `.env` file.

- Open your `hosts` file with administrative privileges using a text editor:

  - **Note for Windows**: If you are in Windows, open the main Windows menu, search for "notepad", right click on it, and select the option "open as Administrator" or similar. Then click the "File" menu, "Open file", go to the directory `c:\Windows\System32\Drivers\etc\`, select the option to show "All files" instead of only "Text (.txt) files", and open the `hosts` file.
  - **Note for Mac and Linux**: Your `hosts` file is probably located at `/etc/hosts`, you can edit it in a terminal running `sudo nano /etc/hosts`.

- Additional to the contents it might have, add a new line with the custom IP (e.g. `192.168.99.150`) a space character, and your fake local domain: `dev.nocturnal-bird-migration.org`.

The new line might look like:

```
192.168.99.100    dev.nocturnal-bird-migration.org
```

- Save the file.
  - **Note for Windows**: Make sure you save the file as "All files", without an extension of `.txt`. By default, Windows tries to add the extension. Make sure the file is saved as is, without extension.

...that will make your computer think that the fake local domain is served by that custom IP, and when you open that URL in your browser, it will talk directly to your locally running server when it is asked to go to `dev.nocturnal-bird-migration.org` and think that it is a remote server while it is actually running in your computer.

To configure it in your stack, follow the section **Change the development "domain"** below, using the domain `dev.nocturnal-bird-migration.org`.

After performing those steps you should be able to open: http://dev.nocturnal-bird-migration.org and it will be server by your stack in `localhost`.

Check all the corresponding available URLs in the section at the end.

### Development with a custom IP URLs

Development URLs, for local development.

Frontend: http://dev.nocturnal-bird-migration.org

Backend: http://dev.nocturnal-bird-migration.org/api/

Automatic Interactive Docs (Swagger UI): https://dev.nocturnal-bird-migration.org/docs

Automatic Alternative Docs (ReDoc): https://dev.nocturnal-bird-migration.org/redoc

PGAdmin: http://dev.nocturnal-bird-migration.org:5050

Flower: http://dev.nocturnal-bird-migration.org:5555

Traefik UI: http://dev.nocturnal-bird-migration.org:8090
