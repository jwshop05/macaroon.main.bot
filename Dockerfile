FROM python:3.9-slim

WORKDIR /app

# requirements 복사 후 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 전체 소스 복사
COPY . .

CMD ["python", "main_bot.py"]