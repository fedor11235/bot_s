docker build --tag python-docker .
docker images
docker run python-docker
docker ps
docker exec -it 93952504a264 bash

pwd
/app

sudo nano /etc/systemd/system/bot.service