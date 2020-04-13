#!/bin/bash

echo -e "Building development..."

sed -i -e 's/STAGE=prod/STAGE=dev2/g' .env

echo -e "Building images.."

docker-compose build --force-rm --compress --parallel 

echo -e "Done"

echo -e "Pushing images to Docker private repo.."

docker-compose push

echo -e "Done..."

