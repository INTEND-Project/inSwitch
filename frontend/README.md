# Intent Frontend
This frontend application provides a simple interface to interact with and test the API from the [intent-back repository](https://github.com/baptisterambour/intent-back).

It is designed primarily as a test tool to explore the API endpoints, send requests, and view responses in a user-friendly way.

## Architecture

![Architecture](architecture.png)

## Getting Started

### Installation

```bash
git clone https://github.com/baptisterambour/intent-front.git
cd intent-front
npm install
```

### Running the Frontend

```bash
npm start
```

This will launch the frontend app and open it in your default browser (usually at http://localhost:3000).

### Running in Docker (development)

You can run the project in a development container with live reload (HMR) using the provided `docker-compose.yml`.

1. Build and start the container (binds host port 3000):

```bash
docker compose up --build
```

2. Open http://localhost:3000 in your browser.

Notes:
- The dev server is configured to bind to `0.0.0.0` so the container is reachable from your host.
- Development environment variables are loaded from `.env.development`. Example values:

```
HOST=0.0.0.0
CHOKIDAR_USEPOLLING=true
REACT_APP_API_BASE=http://localhost:8000
```

Only variables prefixed with `REACT_APP_` will be embedded into the client bundle and accessible from `process.env` in your code (e.g. `process.env.REACT_APP_API_BASE`). Do not store secrets in these variables.