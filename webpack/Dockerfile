FROM node:12-alpine

ENV NODE_OPTIONS="--max-old-space-size=2048"

WORKDIR /app

COPY package.json /app/
COPY yarn.lock /app/

RUN yarn install --frozen-lockfile

COPY . /app/

CMD ["yarn", "production"]
