
FROM python:3.9
COPY . /app
WORKDIR /app
RUN apt update && pip install -r /app/requirements.txt
ENTRYPOINT bash run.sh