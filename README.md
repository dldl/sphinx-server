# Docker-Sphinx

Docker-Sphinx allows you to build Sphinx documentation using a lightweight docker
image based on Alpine.

## Installation

To run a container, clone this repository at the root of your documentation project.
You may use a git submodule.

Add a *.credentials* file following the `username:password` syntax. Documentation
currently only supports authentication using HTTP authentication. It can't be
disabled.

## Usage

### Image creation

Build the image using the following command :

```sh
docker build -t documentation-image .
```

Once the image is built, you can run the documentation in development or production
mode using one of the following commands :

### Container creation

**Production mode:**

```sh
docker run -itd -v "$(pwd)":/web -p 8000:8000 --name documentation-server documentation-image
```

The web server will be listening on `8000` port. Of course, you can change it to your
needs. All the files in the current directory will be mount in the container.

**Developement mode:**

```sh
docker run -itd -v "$(pwd)":/web -p 35729:35729 -p 8000:8000 -e ENV=dev --name documentation-server documentation-image
```

A websocket will be listening on `35729` port to automatically refresh the pages
after a change.

The web server will be listening on `8000` port. All the files in the current
directory will be mount in the container.

### Interacting with the server

- To stop the server, use `docker stop documentation-server`
- To start the server, use `docker start documentation-server`
- To delete the server, use `docker rm -v documentation-server`

You can use the following command to open a shell into the container :

```sh
docker exec -it documentation-server /bin/sh
```

You can then run commands like `make html` to build the documentation automatically.
