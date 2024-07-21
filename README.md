
# Mail relay

This is a simple mail relay that can be used internally to interface with an external mail provider. There are alternatives (namely [grafana/smtprelay](https://github.com/grafana/smtprelay)), but they ended up not working with my ISP's SMTP servers for some reason, which is why I started this project.

## Usage

A configuration sample is provided in [`config-sample.yml`](./config-sample.yml).

### Run with Docker

Start by building the container :

```bash
docker build . -t mail-relay
```

Then, run with the cli :

```bash
docker run --name smtp_relay \
    -p 25:5025 \
    -v '/path/to/conf:/conf:ro' \
    --user 1000:1000 \
    mail-relay:latest
```

Or using docker-compose :

```yaml
version: "3.9"
services:
  relay:
    image: mail-relay:latest
    container_name: smtp_relay
    ports:
      - "25:5025"
    volumes:
      - '/path/to/conf:/conf:ro'
    user: "1000:1000"
```

> [!IMPORTANT]
> The configuration file in `/path/to/conf` must be named `config.yml`.

### Run on host

Simply install the dependencies and run the server :

```bash
pip install -r requirements.txt
./relay.py --conf ./config.yaml
```
