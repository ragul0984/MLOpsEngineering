FROM python:3.9-alpine

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --timeout 100 --retries 10 -r requirements.txt

CMD ["python", "run.py", "--input", "data.csv", "--config", "config.yaml", "--output", "metrics.json", "--log-file", "run.log"]