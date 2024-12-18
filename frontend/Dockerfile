# Use official Node.js image
FROM node:14

WORKDIR /app

# Copy package and install dependensies
COPY package.json ./
RUN npm install

# Copy app files
COPY . .

# Build app
RUN npm run build

# Install Nginx
FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html

# Copy Nginx conf
COPY nginx.conf /etc/nginx/nginx.conf

# Launch Nginx
CMD ["nginx", "-g", "daemon off;"]
