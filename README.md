```sh
docker run -d \
  --name imdb \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  -v imdb_data:/var/lib/postgresql/data \
  betafcc/imdb-postgres:latest
```
