FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libpq-dev \
    gcc \
    curl \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "rental_system.wsgi:application", "--bind", "0.0.0.0:8000"]
