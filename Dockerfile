FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /electronics_app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        gettext \
        default-libmysqlclient-dev \
        build-essential \
        pkg-config \
        && apt-get clean

COPY . .

RUN pip install --upgrade pip
RUN pip install mysqlclient
RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]