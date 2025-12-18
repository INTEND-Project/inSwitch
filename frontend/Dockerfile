FROM node:18-alpine
WORKDIR /app

# Install dependencies
COPY package*.json ./
# Use npm install in the container to avoid lockfile mismatch during CI in this dev-focused image.
# In production builds it's preferred to keep package-lock.json in sync and use `npm ci`.
RUN npm install

# Copy source for live development
COPY . .

# Ensure CRA dev server binds to container interface
ENV HOST=0.0.0.0
# Optional: enable polling for file changes in some mounted filesystems
ENV CHOKIDAR_USEPOLLING=true

EXPOSE 3000
CMD ["npm", "start"]
