FROM python:3.12-alpine

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "-b", ":5000", "flask_main:app"]
