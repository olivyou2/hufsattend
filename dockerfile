FROM python:latest

ADD . /app
RUN pip install -r /app/requirements.txt
ENTRYPOINT [ "python", "/app/app.py" ]