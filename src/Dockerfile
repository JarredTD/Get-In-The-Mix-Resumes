FROM python:3.12-slim

ENV DATABASE_URI=sqlite:///user_resume_data.db
ENV FLASK_APP=../run.py

RUN mkdir /src
RUN mkdir /src/app
WORKDIR /src/

COPY ./run.py /src/
COPY ./app /src/app

RUN pip3 install --no-cache-dir -r app/app-requirements.txt

WORKDIR /src/app
RUN touch user_resume_data.db
RUN flask db upgrade

WORKDIR /src
EXPOSE 8080
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "run:app"]
