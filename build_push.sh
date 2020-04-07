#!/bin/bash
docker-compose build --force-rm --compress --parallel 
docker-compose push

