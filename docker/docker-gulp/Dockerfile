FROM mhart/alpine-node:7.7
MAINTAINER Cristian Spoiala <cristian@spoiala.ro>

RUN npm i -g gulp && \
    rm -rf /tmp/*

COPY commands /commands

ENTRYPOINT ["/commands/entry.sh"]

CMD ["gulp-prod"]
