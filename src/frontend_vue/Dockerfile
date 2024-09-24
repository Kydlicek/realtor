# Stage 1: Build the Vue frontend
FROM node:18-alpine AS build-stage

WORKDIR /app

# Install all dependencies for building
COPY package.json package-lock.json ./
RUN npm ci

# Copy the rest of the application code
COPY . .

# Build the Vue app for production
RUN npm run build

# Stage 2: Production image
FROM nginx:1.21-alpine AS production-stage

# Copy the build output from the build stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
