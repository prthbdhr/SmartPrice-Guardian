# Docker Deployment Guide

## Quick Start

### Build the Docker Image
```bash
docker build -t smartprice-guardian .
```

### Run with Docker
```bash
docker run -d -p 8000:8000 --name smartprice-guardian smartprice-guardian
```

### Run with Docker Compose
```bash
docker-compose up -d
```

## Access the Application

- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Docker Commands

### View Logs
```bash
docker logs smartprice-guardian
```

### Stop Container
```bash
docker stop smartprice-guardian
```

### Remove Container
```bash
docker rm smartprice-guardian
```

### Restart Container
```bash
docker restart smartprice-guardian
```

## Docker Compose Commands

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
```

### Rebuild and Restart
```bash
docker-compose up -d --build
```

## Testing the API

```bash
# Health check
curl http://localhost:8000/health

# Get SKU summary
curl http://localhost:8000/data/summary/SKU-A

# Get pricing recommendation
curl http://localhost:8000/pricing/recommendation/SKU-A

# Get demand forecast
curl http://localhost:8000/forecast/SKU-A
```

## Environment Variables

The application can be configured using environment variables in docker-compose.yml:

```yaml
environment:
  - PYTHONUNBUFFERED=1
  - PORT=8000
```

## Volume Mounts

Data files are mounted as volumes to allow updates without rebuilding:

```yaml
volumes:
  - ./data:/app/data
```

## Production Deployment

For production, consider:

1. Use specific version tags instead of `latest`
2. Set up proper logging and monitoring
3. Configure resource limits
4. Use secrets management for sensitive data
5. Set up health checks and auto-restart policies
