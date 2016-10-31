# Sphinx-Server

[![](https://images.microbadger.com/badges/image/dldl/sphinx-server.svg)](https://microbadger.com/images/dldl/sphinx-server)

Sphinx-Server allows you to build *Sphinx documentation* using a Docker
image based on Alpine.

**Functionnalities:**

- *Sphinx documentation* served by a python server
- UML support with *PlantUML*
- `dot` support with *Graphviz*
- *Autobuild* with sphinx-autobuild
- HTTP *authentication*

**Limitations:**

- This image is not bundled with LaTex but you can generate *.tex* files and
  compile them outside of the container

## Installation

### With Docker Hub

Pull the image from Docker Hub using:

```sh
docker pull dldl/sphinx-server
```

### From source

Clone this repository on your computer and build the image using the following
command:

```sh
docker build -t dldl/sphinx-server .
```

## Usage

You may add a *.sphinx-server.yml* file at the root of your project
documentation if you want to use a custom configuration. You can see the default
*.sphinx-server.yml* in this repository that will be used if you don't add
yours.

### Container creation

**Without autobuild (production mode):**

If you want to enable HTTP authentication, just add a *.sphinx-server.yml* file
at the root of your project documentation and add a `credentials` section.

Run the following command at the root of your documentation:

```sh
docker run -itd -v "$(pwd)":/web -p 8000:8000 --name sphinx-server dldl/sphinx-server
```

**With autobuild enabled:**

Add a *.sphinx-server.yml* file at the root of your project documentation with
`autobuild` set to true. You may add folders and files to the `ignore` list.

Run the following command at the root of your documentation:

```sh
docker run -itd -v "$(pwd)":/web -p 35729:35729 -p 8000:8000 --name sphinx-server dldl/sphinx-server
```

The web server will be listening on port `8000`. Of course, you can change it to
your needs. All the files in the current directory will be mount in the
container. A websocket will be listening on port `35729` to automatically
refresh the pages after a change.

### Interacting with the server

- To stop the server, use `docker stop sphinx-server`
- To start the server, use `docker start sphinx-server`
- To remove the server, use `docker rm -v sphinx-server`

You can use the following command to open a shell into the container:

```sh
docker exec -it sphinx-server /bin/sh
```

You can then run commands like `make html` to build the documentation.
