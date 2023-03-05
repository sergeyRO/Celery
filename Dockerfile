FROM python:3.9
COPY . /app
WORKDIR /app
RUN apt-get install python3-opencv && pip install -r ./app/requirements.txt
ENTRYPOINT bash run.sh