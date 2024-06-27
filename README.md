# Flask IP Map

## @TODO
[] Change logic to not allow loading into visits var in map.html. visible from curl. populates in html when it should just dynamically pull

devmaks.biz

env var:
IPINFO_TOKEN
https://ipinfo.io

local build:
```bash
docker build -t flask-ip-map .
docker run -e IPINFO_TOKEN={TOKEN} -p 5000:5000 flask-ip-map
```
