FROM python:3.8
ENV DEBIAN_FRONTEND noninteractive
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y python3-pip && pip3 install matplotlib influxdb flask\
    && apt-get install -y python3-tk 
COPY prog/ /usr/src/app/prog
CMD ["python3", "-m", "prog"]
