FROM python:3.8-slim-buster

COPY . /app
WORKDIR /app

COPY bucket-noti-handle.py ./
COPY requirements.txt ./

RUN pip3 install --upgrade -r requirements.txt

ENTRYPOINT ["python3", "./bucket-noti-handle.py"]
