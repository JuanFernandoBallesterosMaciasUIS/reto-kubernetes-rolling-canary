#!/usr/bin/env bash
# Construye las 4 versiones de la imagen. Docker Desktop comparte las imágenes locales con su Kubernetes.
set -e
cd "$(dirname "$0")/../app"
docker build -q -t reto-app:v1        --build-arg APP_VERSION=v1 --build-arg APP_COLOR=steelblue .
docker build -q -t reto-app:v2        --build-arg APP_VERSION=v2 --build-arg APP_COLOR=seagreen  .
docker build -q -t reto-app:v4-crash  --build-arg APP_VERSION=v4 --build-arg APP_COLOR=firebrick --build-arg FAIL_MODE=crash  .
docker build -q -t reto-app:v3        --build-arg APP_VERSION=v3 --build-arg APP_COLOR=rebeccapurple .
docker images reto-app
