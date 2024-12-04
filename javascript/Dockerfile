FROM node:alpine as base

ENTRYPOINT [ "npm" ]

WORKDIR /TreeService

COPY package.json ./

RUN npm install

COPY . .

CMD ["start"]
