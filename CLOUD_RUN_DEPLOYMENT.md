# Google Cloud Run 部署指南

## 概述

本應用已配置為可在 Google Cloud Run 上運行。主要修改包括：

1. ✅ 使用 Gunicorn 作為 WSGI 服務器（替代 Flask 開發服務器）
2. ✅ 端口配置支援 Cloud Run 的 PORT 環境變數（預設 8080）
3. ✅ 添加了 `.dockerignore` 以優化構建
4. ✅ 更新了健康檢查配置

## 重要注意事項

### ⚠️ 無狀態限制

Google Cloud Run 是**無狀態**的服務，這意味著：

1. **本地文件系統不持久化**：
   - `uploads/` 目錄中的文件在容器重啟後會丟失
   - `logs/` 目錄中的日誌不會持久化
   - `*.db` 數據庫文件不會持久化

2. **建議的解決方案**：
   - **文件上傳**：使用 Google Cloud Storage (GCS) 存儲上傳的文件
   - **日誌**：使用 Cloud Logging（應用日誌會自動發送到 Cloud Logging）
   - **數據庫**：使用 Cloud SQL 或 Cloud Firestore 替代 SQLite

### 🔐 環境變數配置

在 Cloud Run 部署時，需要設置以下環境變數：

```bash
FLASK_ENV=production
PYTHONPATH=/app
PORT=8080  # Cloud Run 會自動設置，無需手動配置
```

**注意**: `GOOGLE_APPLICATION_CREDENTIALS` **不需要**設置，因為應用會自動使用 Cloud Run 的默認憑證。

### 📝 服務帳戶和憑證

1. **Gemini API 認證**：
   - ✅ 應用已配置為自動使用 Cloud Run 的**默認憑證**（Application Default Credentials）
   - ✅ **不需要**在 Docker 映像中包含 JSON 憑證文件
   - ✅ **不需要**設置 `GOOGLE_APPLICATION_CREDENTIALS` 環境變數
   - ✅ 確保 Cloud Run 服務帳戶有 `roles/aiplatform.user` 權限

2. **設置服務帳戶權限**：
   ```bash
   PROJECT_ID=$(gcloud config get-value project)
   gcloud projects add-iam-policy-binding $PROJECT_ID \
     --member="serviceAccount:YOUR_SERVICE_ACCOUNT@${PROJECT_ID}.iam.gserviceaccount.com" \
     --role="roles/aiplatform.user"
   ```

## 部署步驟

### 1. 構建 Docker 映像

```bash
cd hansa-test
docker build -t gcr.io/YOUR_PROJECT_ID/bakudocs:latest .
```

### 2. 推送到 Google Container Registry

```bash
# 配置 Docker 認證
gcloud auth configure-docker

# 推送映像
docker push gcr.io/YOUR_PROJECT_ID/bakudocs:latest
```

### 3. 部署到 Cloud Run

```bash
gcloud run deploy bakudocs \
  --image gcr.io/YOUR_PROJECT_ID/bakudocs:latest \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10 \
  --set-env-vars FLASK_ENV=production,PYTHONPATH=/app \
  --service-account YOUR_SERVICE_ACCOUNT@PROJECT_ID.iam.gserviceaccount.com
```

### 4. 使用 Cloud Build（推薦）

創建 `cloudbuild.yaml`：

```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/bakudocs:$SHORT_SHA', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/bakudocs:$SHORT_SHA']
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'bakudocs'
      - '--image'
      - 'gcr.io/$PROJECT_ID/bakudocs:$SHORT_SHA'
      - '--region'
      - 'asia-east1'
      - '--platform'
      - 'managed'
      - '--allow-unauthenticated'
      - '--memory'
      - '2Gi'
      - '--cpu'
      - '2'
      - '--timeout'
      - '300'
images:
  - 'gcr.io/$PROJECT_ID/bakudocs:$SHORT_SHA'
```

然後執行：

```bash
gcloud builds submit --config cloudbuild.yaml
```

## 本地測試

在部署到 Cloud Run 之前，建議先在本地測試：

```bash
# 構建映像
docker build -t bakudocs:test .

# 運行容器
docker run -p 8080:8080 \
  -e FLASK_ENV=production \
  -e PORT=8080 \
  bakudocs:test

# 測試應用
curl http://localhost:8080/login
```

## 性能優化建議

1. **記憶體配置**：
   - 建議至少 2Gi（處理大文件時可能需要更多）
   - OCR 和 PDF 處理需要較多記憶體

2. **CPU 配置**：
   - 建議至少 2 個 CPU
   - 多線程處理時需要更多 CPU

3. **超時設置**：
   - 文件處理可能需要較長時間，建議設置為 300 秒或更高

4. **並發設置**：
   - Gunicorn workers: 2（根據 CPU 數量調整）
   - Gunicorn threads: 2
   - Cloud Run max instances: 根據需求設置

## 故障排除

### 問題：應用無法啟動

檢查日誌：
```bash
gcloud run services logs read bakudocs --limit 50
```

### 問題：端口錯誤

確保應用監聽 `0.0.0.0` 和環境變數 `PORT`（Cloud Run 會自動設置）

### 問題：文件上傳失敗

檢查 Cloud Run 的記憶體限制，大文件處理可能需要更多記憶體

## 後續改進建議

1. **遷移到 Cloud Storage**：
   - 修改文件上傳邏輯，直接上傳到 GCS
   - 修改文件讀取邏輯，從 GCS 讀取

2. **遷移到 Cloud SQL**：
   - 將 SQLite 遷移到 Cloud SQL (PostgreSQL/MySQL)
   - 更新數據庫連接配置

3. **添加監控**：
   - 使用 Cloud Monitoring 監控應用性能
   - 設置告警規則

4. **CDN 配置**：
   - 使用 Cloud CDN 加速靜態資源

5. **認證配置**：
   - 如果需要身份驗證，配置 Cloud Run 的 IAM 權限
   - 或使用 Firebase Authentication

