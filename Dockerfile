FROM python:3.7.3
MAINTAINER Rama
LABEL version="1.2"

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0" ]