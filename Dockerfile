FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r ./app/requirements.txt
#RUN apt update && apt-get install -y python3-opencv && pip install -r requirements.txt
ENTRYPOINT bash run.sh