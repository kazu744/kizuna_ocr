FROM node:20-alpine

WORKDIR /app

# 依存ファイルコピー
COPY package*.json ./
RUN npm ci

# ソースコードコピー
COPY . .

ENV HOST=0.0.0.0
EXPOSE 3000

CMD ["npm", "run", "dev"]