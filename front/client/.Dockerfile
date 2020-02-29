FROM node:13.8.0-buster-slim
WORKDIR /client
COPY package*.json /client/
RUN npm install
COPY . /client
CMD ["npm", "start"]
