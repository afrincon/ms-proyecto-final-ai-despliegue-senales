FROM node:hydrogen-slim as build-stage

RUN mkdir -p /app

WORKDIR /app

COPY package.json /app

RUN npm install

COPY . /app

RUN npm run build


FROM nginx

COPY --from=build-stage /app/dist/front-ms /usr/share/nginx/html
