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

# 複製程式碼（排除不必要的文件）
COPY . .

# 建立必要資料夾
RUN mkdir -p logs uploads static/user_logos

# 環境變數
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Cloud Run 使用環境變數 PORT，預設為 8080
ENV PORT=8080
EXPOSE 8080

# 建立非 root 用戶，使用主機用戶的 UID/GID
ARG USER_ID=1001
ARG GROUP_ID=1001
RUN groupadd -g $GROUP_ID appuser && \
    useradd -u $USER_ID -g $GROUP_ID -m -s /bin/bash appuser && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app
USER appuser

# 健康檢查 - Cloud Run 會自動處理健康檢查，這裡使用預設端口 8080
# 注意：Cloud Run 的健康檢查是通過 HTTP 請求進行的，不需要這裡的 HEALTHCHECK
# 保留此處僅為本地測試使用
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/login || exit 1

# 使用 Gunicorn 啟動應用（適合生產環境）
# Cloud Run 會自動設置 PORT 環境變數
CMD exec gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 2 --threads 2 --timeout 300 --access-logfile - --error-logfile - app:app
