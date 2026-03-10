#!/bin/bash

apt-get update

apt-get install -y nodejs npm chromium chromium-driver fonts-liberation

npm install -g lighthouse

pip install -r requirements.txt

which chromium
which google-chrome

uvicorn main:app --host 0.0.0.0 --port $PORT