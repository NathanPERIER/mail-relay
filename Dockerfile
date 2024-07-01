FROM alpine:edge

RUN mkdir -v /opt/mail-relay /conf && apk update && apk add --update --no-cache python3 py3-pip && ln -sf python3 /usr/bin/python

WORKDIR /opt/mail-relay

COPY src ./src
COPY requirements.txt relay.py testmail.py ./
RUN rm /usr/lib/python3.*/EXTERNALLY-MANAGED && pip3 install -r requirements.txt && rm requirements.txt

ENTRYPOINT ["python3", "relay.py"]
CMD ["--conf", "/conf/config.yml"]