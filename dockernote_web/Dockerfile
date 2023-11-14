FROM python:3.12

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/app

WORKDIR /code/app
CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0:8080