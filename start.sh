#!/bin/bash

apt-get update
apt-get install -y nodejs npm chromium

npm install -g lighthouse

pip install -r requirements.txt

uvicorn main:app --host 0.0.0.0 --port $PORT