
# Mail relay

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

> Note: the configuration file in `/path/to/conf` must be named `config.yml`.

### Run on host

Simply install the dependencies and run the server :

```bash
pip install -r requirements.txt
./relay.py --conf ./config.yaml
```
