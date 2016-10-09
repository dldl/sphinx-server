FROM alpine

MAINTAINER Loïc Pauletto <loic.pauletto@gmail.com>
MAINTAINER Quentin de Longraye <quentin@dldl.fr>

RUN apk add --no-cache --virtual --update py-pip make wget ca-certificates ttf-dejavu openjdk8-jre graphviz && \

    pip install --upgrade pip && \
    pip install sphinx==1.4.6 sphinx_rtd_theme sphinxcontrib-plantuml sphinx_autobuild && \

    wget http://downloads.sourceforge.net/project/plantuml/plantuml.jar -P /opt/

WORKDIR /web

COPY ./server.py .

EXPOSE 8000 35729

CMD ["python", "./server.py"]
