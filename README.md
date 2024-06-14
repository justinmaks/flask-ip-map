# Flask IP Map

devmaks.biz

env var:
IPINFO_TOKEN
https://ipinfo.io

local build:
```bash
docker build -t flask-ip-map .
docker run -e IPINFO_TOKEN={TOKEN} -p 5000:5000 flask-ip-map
```