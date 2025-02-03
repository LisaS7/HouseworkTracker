git pull origin main
docker stop houseworktracker || true
docker rm houseworktracker || true
docker build -t houseworktracker:latest .
docker run -d --name houseworktracker -p 8000:8000 houseworktracker:latest