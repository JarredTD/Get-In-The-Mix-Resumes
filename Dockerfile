FROM python:3.12-slim

RUN mkdir src
RUN mkdir src/app
WORKDIR /src


COPY ./app /src/app

RUN pip3 install --no-cache-dir -r app/app-requirements.txt

EXPOSE 8080

ENV FLASK_APP=app/__init__.py

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
