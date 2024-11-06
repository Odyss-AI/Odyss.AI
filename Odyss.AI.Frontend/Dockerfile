# Stage 1: Build the Vite app
FROM node:18-alpine AS build
 
# Set working directory
WORKDIR /app
 
# Copy package.json and package-lock.json
COPY package*.json ./
 
# Install dependencies
RUN npm install
 
# Copy the rest of the application
COPY . .
 
# Build the application
RUN npm run build
 
# Stage 2: Serve with NGINX
FROM nginx:alpine
 
# Copy the built files from the build stage to NGINX's web directory
COPY --from=build /app/dist /usr/share/nginx/html
 
# Expose port 80
EXPOSE 443
 
# Start NGINX server
CMD ["nginx", "-g", "daemon off;"]