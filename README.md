## forkin
This application runs a flask service that allows a user to fork this application to their own GitHub account

## Two Ways To Try It Out

### Docker Desktop

[Open in Docker Dev Environment](https://open.docker.com/dashboard/dev-envs?url=https://github.com/andrew-pettus/forkin/tree/main)

After running this project as a container, build the service with

```
docker build --pull --rm -f "flask_docker/Dockerfile" -t forkin:latest "flask_docker"
```

After the container is built, start the service with

```
docker run --rm -it -p 5000:5000/tcp forkin:latest
```

Using a browser, navigate to http://127.0.0.1:5000/



### Build Locally From Source

```bash
git clone https://github.com/andrew-pettus/forkin.git
cd forkin
```
After cloning this project locally, build the service with
```
docker build --pull --rm -f "flask_docker/Dockerfile" -t forkin:latest "flask_docker"
```
After the container is built, start the service with
```
docker run --rm -it -p 5000:5000/tcp forkin:latest
```
Using a browser, navigate to http://127.0.0.1:5000/
