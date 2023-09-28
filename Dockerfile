FROM python:3.10.13-slim-bullseye

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /
# ENV PYTHONPATH "${PYTHONPATH}:/"

COPY . .