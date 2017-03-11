FROM mhart/alpine-node:7.7
MAINTAINER Cristian Spoiala <cristian@spoiala.ro>

RUN apk add --update bash git

RUN npm i -g gulp-cli && \
    rm -rf /tmp/*

COPY commands /commands

ENTRYPOINT ["/commands/entry.sh"]

CMD ["default"]
