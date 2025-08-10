# Python 슬림 이미지 사용
FROM python:3.9-slim

# 작업 디렉터리 정하기
WORKDIR /app

# requirements.txt 복사
COPY requirements.txt .

# 라이브러리 설치
RUN pip install --no-cache-dir -r requirements.txt

# 소스 전체 복사 (main_bot.py 포함)
COPY . .

# 봇 실행
CMD ["python", "main_bot.py"]