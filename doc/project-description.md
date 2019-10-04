# Portia: an exotic pet store
## Architecture
This project follows a 4-tire Django project architecture: HTML frontend + experience service APIs + entity / model APIs + backend database. Every tier lives in a separate Docker container, each of which is orchestrated by `docker-compose.yml`
### HTML frontend

### experience service APIs
 - Explnanation: the experience layer will invoke entity APIs via HTTP and recieve JSON respones. Similarly, it will provide HTTP / JSON APIs to the HTML templates
 - Container image: `tp33/django`
 - Container name: data-service
 - Run command (will be integrated into `docker-compose.yml`): `sudo docker run -it --name data-service -v /mnt/documents-local/CS4260/internet-scale-app/data-service:/app tp33/django`
 - API design
    - CRUD services for entity `Pet` and `User`
    - ...

### entity / model APIs
 - Container image: `tp33/django`
 - Container name: web
 - Run command: brought up by `docker-compose.yml`
 - 

### backend database
 - Container image: `mysql:latest`
 - Container name: `mysql`
 - Run command: `sudo docker run --name mysql -d -e MYSQL_ROOT_PASSWORD='$3cureUS' -v /mnt/documents-local/CS4260/internet-scale-app/db:/var/lib/mysql  mysql:latest`
 - Network command: `sudo docker network connect internet-scale-app_backend mysql`


## Common gotchas
 ### DB container configuration
 - Container `web` and requires a mysql container with username `'www'@'%'` and password `$cureUS` and a database named `cs4260` set up. Otherwise, docker compose will not bring up any contiainer. 