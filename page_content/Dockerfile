FROM python:3

RUN apt-get update; apt-get clean

RUN apt-get install -y wget

COPY google-chrome-stable_113.0.5672.63-1_amd64.deb google-chrome-stable_113.0.5672.63-1_amd64.deb

RUN apt-get update && apt-get install -y gcc python3-dev python3-pip default-libmysqlclient-dev ffmpeg libsm6 libxext6 ./google-chrome-stable_113.0.5672.63-1_amd64.deb

COPY requirements.txt .

RUN pip3 install -r requirements.txt

WORKDIR /src

COPY . /src

CMD ["src/API.py"]

ENTRYPOINT ["python3"]
