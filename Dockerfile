FROM python:3.10-slim

WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsqlite3-dev \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-chi-tra \
    poppler-utils \
    libpoppler-cpp-dev \
    gcc \
    g++ \
    curl \
 && rm -rf /var/lib/apt/lists/*

# 複製 requirements 並安裝依賴
COPY requirements.txt .
RUN pip uninstall -y urllib || true
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# 複製程式碼
COPY . .

# 建立必要資料夾
RUN mkdir -p logs uploads static/user_logos

# 環境變數
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

EXPOSE 5001

# 建立非 root 用戶，使用主機用戶的 UID/GID
ARG USER_ID=1001
ARG GROUP_ID=1001
RUN groupadd -g $GROUP_ID appuser && \
    useradd -u $USER_ID -g $GROUP_ID -m -s /bin/bash appuser && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app
USER appuser

# 健康檢查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5001/login || exit 1

# 啟動 Flask (建議換 gunicorn)
CMD ["python", "app.py"]
