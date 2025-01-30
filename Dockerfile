FROM postgres:17

RUN apt-get update && apt-get install -y \
    python3 \
    wget \
    gzip \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY imdblib /app/imdblib
COPY init.sh /docker-entrypoint-initdb.d/init.sh
RUN chmod +x /docker-entrypoint-initdb.d/init.sh

ENV POSTGRES_USER=imdb
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=imdb
ENV POSTGRES_HOST_AUTH_METHOD=trust
ENV PYTHONUNBUFFERED=1
