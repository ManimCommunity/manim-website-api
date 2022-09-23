# Maintenance

# Updating the Server

After sshing into the machine:
```bash
sudo apt update
sudo apt full-upgrade
```

# Update Docker Services

After sshing into the machine:
```bash
cd /srv/manim-website-api/server/
sudo docker-compose pull
sudo docker-compose build --parallel --no-cache
sudo docker-compose up -d
sudo docker system prune --all --force
```
