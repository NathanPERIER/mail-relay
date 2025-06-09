FROM alpine:latest

RUN --mount=type=bind,source=./requirements.txt,target=/tmp/requirements.txt \
    mkdir -v /opt/mail-relay /conf \
    && apk update \
    && apk add --update --no-cache python3 py3-pip \
    && ln -sf python3 /usr/bin/python \
    && pip3 install --break-system-packages -r /tmp/requirements.txt

WORKDIR /opt/mail-relay

COPY src ./src
COPY relay.py testmail.py ./

ENTRYPOINT ["python3", "relay.py"]
CMD ["--conf", "/conf/config.yml"]