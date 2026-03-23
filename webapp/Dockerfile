FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
COPY app.py ./
COPY templates ./templates
COPY exports ./exports

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]