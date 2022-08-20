# About

This little Docker container will listen for http POST, and writes received json to a file
## How to

### Docker

Clone this repo and then add this to your `docker-compose.yml` file:

```yaml
  http2json:
    build: https://github.com/itec78/http2json.git
    container_name: http2json  # optional
    environment:
      - "LOG_LEVEL=DEBUG"  # optional, defaults to INFO
    volumes:
      - /data/http2json:/data
    restart: unless-stopped
  ```
  
