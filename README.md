```bash
 docker build -t data_collector:latest .
 docker network create exo
 docker run --network=exo data_collector:latest
```
