git pull origin main || { echo "error"; exit 1; }
docker stop houseworktracker || true
docker rm houseworktracker || true
docker build -t houseworktracker:latest .
docker run -d --name houseworktracker -p 8000:8000 houseworktracker:latest