# Monitoring and Observability

# Overview
- Using monitoring tools like **Prometheus, Grafana and Grafana Loki** to monitor the health of the servers.
- The servers are uvicorn servers created with **FastAPI**
- The architecture looks like this:


# Prerequisites
- As shown in the figure, you will require minimum two nodes, out of which one node will be the *Monitoring Server* and rest would be *Server-emulators*.
- Knowledge about Docker containers, images, docker-compose and ports-mapping.
- Knowledge about IPv4 address networking.

# Server-emulator Setup
- I have already created a docker image of my server emulator so you can just pull the image.
```bash
docker pull atharva25s/server-emulator:latest
```
```bash
docker run -d --name <container_name> -p 8000:8000 atharva25s/server-emulator:latest
```

- Verify the container's state.
```bash
docker ps
```

- Viewing logs of the server continuously
``` bash
docker logs -f <container_name>
```

- Setting up loki url. You will have to go inside your container and replace *Loki URL* with ipv4 public address of your monitoring server.
```bash
docker exec -it <container_name> bash
```
```bash
nano main.py
```

- Look for this and change the URL with IPv4 public address of you monitoring server.
```bash
loki_handler = logging_loki.LokiQueueHandler(
    log_queue,
    url="http://<LOKI_URL>/loki/api/v1/push",  # Change to your Loki URL
    tags={"application": "fastapi-emulator"},
    version="1"
)
```

- Restart the container
```bash
docker restart <container_name>
```

- Now based on how much servers you want these aforementioned instructions can be multiplied.

# Watch-server setup
- Copy the files from [Watch-Server directory](Watch-Server) into the root directory of your monitoring server.

- Edit the **prometheus.yml**
```bash
nano prometheus.yml
```

- Edit the targets and put the IPv4 Public address of your *server-emulators*.
- You can add or remove targets based on your requirements.
- Start all 3 containers of *Prometheus*,  *Grafana*, and *Loki*
```bash
docker-compose up
```

# Grafana Dashboard
- Go onto the Grafana login with
    - Username: admin
    - Password: admin
```bash
http://<PUBLIC_IP_MONITORING_SERVER>:3000
```
- Setup your datasources
- And then you can create your dashboard.

# Here's a video of the end results
[![Monitoring & Observability with Prometheus, Grafana & Loki](assets\Grafana.png)](https://youtu.be/ZgnwUhjTIro)

