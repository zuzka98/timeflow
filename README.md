# Official documentation
<a href="https://dyvenia.github.io/timeflow/" target="_blank">https://dyvenia.github.io/timeflow/</a>

# Local Setup instructions

1) Install with pip all libs in requirements.txt `pip install -r requirements`

2) `uvicorn main:app --reload`

3) `uvicorn backend.main:app --reload`

# Docker instructions for DEV 

1) Run docker-compose up
```bash
docker-compose -f docker-compose-dev.yaml
```
*If you don't wish to look at the docker logs, run the command `docker-compose up` with the flag `-d` instead of `docker-compose up`*
```bash
docker-compose up -d
```