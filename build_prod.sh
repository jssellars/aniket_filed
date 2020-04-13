#!/bin/bash

echo -e "Building production..."

sed -i -e 's/STAGE=dev2/STAGE=prod/g' .env

echo -e "Building images.."

docker-compose build --force-rm --compress --parallel 

echo -e "Done"

echo -e "Pushing images to Docker private repo.."

docker-compose push

echo -e "Done..."