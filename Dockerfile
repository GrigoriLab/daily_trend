FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD python manage.py migrate && python manage.py loaddata user.json && celery -A daily_trend worker --beat --loglevel=info & python manage.py runserver 0.0.0.0:8000