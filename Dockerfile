FROM python:3.11-slim

WORKDIR /app

COPY req.txt .

RUN pip install --no-cache-dir -r req.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD python manage.py migrate && gunicorn misstantra.wsgi:application --bind 0.0.0.0:8000