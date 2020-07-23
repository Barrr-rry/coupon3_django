#!/bin/sh

docker exec -it coupon3-django-web python before_deploy.py &
docker-compose -f docker-compose_test.yml up --build -d &
docker exec -it coupon3-django-web python after_deploy.py