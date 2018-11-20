FROM node:10-alpine
WORKDIR /app
COPY package.json /app/
COPY yarn.lock /app/
RUN npm install --global yarn && yarn install
COPY * /app/
CMD ["yarn", "production"]
