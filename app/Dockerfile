FROM node:14-alpine AS build

WORKDIR /usr/src/app/app

COPY package.json .
COPY package-lock.json .

RUN npm install

COPY . ./

RUN npm run build

FROM nginx:1.19-alpine
COPY --from=build /usr/src/app/app/public /usr/share/nginx/html
