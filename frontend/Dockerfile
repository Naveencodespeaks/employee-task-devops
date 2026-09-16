# Stage 1: build the static React bundle with Node.
FROM node:20-slim AS build

WORKDIR /app

# VITE_API_BASE_URL is baked into the JS bundle at build time (Vite
# resolves import.meta.env.* during `vite build`), so it must be passed
# as a build arg, not a runtime env var.
ARG VITE_API_BASE_URL=http://localhost:8000
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

COPY package.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: serve the built files with Nginx. Final image has no Node,
# no source code, no node_modules -- just static files + Nginx.
FROM nginx:1.27-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
