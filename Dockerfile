FROM node:18-bullseye

# install python + chromium
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# install lighthouse
RUN npm install -g lighthouse

WORKDIR /app

COPY . .

RUN pip3 install fastapi uvicorn pydantic

ENV PORT=10000

CMD uvicorn main:app --host 0.0.0.0 --port 10000