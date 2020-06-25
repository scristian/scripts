#FROM mhart/alpine-node:7.7
FROM mhart/alpine-node:10.13
MAINTAINER Cristian Spoiala <cristian@spoiala.ro>

RUN apk add --update bash git

RUN apk add --no-cache make gcc g++ python

RUN npm i -g gulp-cli && \
    rm -rf /tmp/*

COPY commands /commands

ENTRYPOINT ["/commands/entry.sh"]

CMD ["default"]
