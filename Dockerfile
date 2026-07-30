@'
FROM python:3.12-slim

WORKDIR /app

COPY test32.py .

CMD ["python", "test32.py"]
'@ | Set-Content -Encoding utf8 Dockerfile