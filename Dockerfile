FROM python:3.10
WORKDIR /usr/src/app
COPY requirements.txt .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    yasm \
    unzip

RUN wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz \
    && tar -xf ffmpeg-release-amd64-static.tar.xz \
    && rm ffmpeg-release-amd64-static.tar.xz

RUN mv ffmpeg-*-static/ffmpeg /usr/local/bin/ffmpeg

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python", "MVP/manage.py", "runserver", "0.0.0.0:8000"]