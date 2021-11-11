FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/artway

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python3 manage.py collectstatic --noinput

CMD sh -c "python3 manage.py migrate && python3 manage.py createsuperuser --noinput ; gunicorn --bind 0.0.0.0:8080 project.wsgi"
