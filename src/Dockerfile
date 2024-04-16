FROM python:3.12-slim

RUN mkdir /src
RUN mkdir /src/app
WORKDIR /src/

# These values are hardcoded as they are meant to be locally hosted, and thus
# are not a security risk
#
# Please generate new values/files if you are going to host this publically
ENV DATABASE_URI=sqlite:///user_resume_data.db
ENV FLASK_APP=../run.py
ENV SAVE_PATH=app/static/word/resume.docx
ENV FLASK_SECRET_KEY=d9593945b43c1c3607ac454ede6386fd0e1b3f7a5c55339edaf84e59fbb0a569

COPY ./run.py /src/
COPY ./app /src/app

RUN pip3 install --no-cache-dir -r app/app-requirements.txt

WORKDIR /src/app
RUN touch user_resume_data.db
RUN flask db upgrade

WORKDIR /src
EXPOSE 8080
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "run:app"]
