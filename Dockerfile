FROM python:3.10
WORKDIR /usr/src/app
COPY requirements.txt .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y ffmpeg

COPY . .

EXPOSE 8000

CMD [ "python", "MVP/manage.py", "runserver", "0.0.0.0:8000"]