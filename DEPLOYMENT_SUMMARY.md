# Cloud Run 部署配置總結

## ✅ 已完成的修改

### 1. Gemini API 認證改進 ✅

**修改文件**:
- `analyzers/clients/gemini_client.py`
- `utils_gemini.py`

**變更內容**:
- ✅ 優先使用 Cloud Run 的**默認憑證**（Application Default Credentials）
- ✅ 自動偵測環境，在 Cloud Run 上無需 API key 文件
- ✅ 本地開發時仍可使用文件憑證作為後備方案

**優勢**:
- 🔒 更安全：不需要在 Docker 映像中包含敏感憑證文件
- 🚀 更簡單：Cloud Run 自動處理認證
- ✅ 符合 Google Cloud 最佳實踐

### 2. GitHub 自動部署配置 ✅

**新增文件**:
- `cloudbuild.yaml` - Cloud Build 配置文件
- `GITHUB_DEPLOYMENT.md` - 詳細部署指南
- `GITHUB_DEPLOYMENT_QUICK.md` - 快速參考指南

**功能**:
- ✅ 從 GitHub 推送代碼自動觸發部署
- ✅ 自動構建 Docker 映像
- ✅ 自動部署到 Cloud Run
- ✅ 支援版本標籤（$SHORT_SHA）

### 3. Docker 配置優化 ✅

**修改文件**:
- `Dockerfile` - 已優化為 Cloud Run 標準
- `.dockerignore` - 已更新以排除不必要文件

**變更**:
- ✅ 使用 Gunicorn（生產級 WSGI 服務器）
- ✅ 端口配置為 8080（Cloud Run 標準）
- ✅ 支援 PORT 環境變數
- ✅ 排除敏感文件和臨時文件

### 4. 檔案清理 ✅

**已刪除文件**:
- ✅ `test_layout.html` - 測試文件
- ✅ `verify_fix.html` - 測試文件
- ✅ `logo_preview.html` - 測試文件
- ✅ `fix_tokens_in_history.py` - 臨時腳本
- ✅ `history.pkl` - 臨時文件

### 5. Git 配置更新 ✅

**修改文件**:
- `.gitignore` - 已更新

**新增排除規則**:
- ✅ Google Cloud 憑證文件（*.json）
- ✅ 測試文件
- ✅ 臨時文件和緩存
- ✅ MacOS 系統文件（__MACOSX/）

## 📋 部署前檢查清單

### 必需步驟

- [ ] 確保 Google Cloud 專案已建立
- [ ] 啟用 Cloud Build API
- [ ] 啟用 Cloud Run API
- [ ] 啟用 Vertex AI API（用於 Gemini）
- [ ] 在 GitHub 上建立倉庫
- [ ] 在 Cloud Console 中連接 GitHub 倉庫
- [ ] 建立 Cloud Run 服務帳戶並授予權限
- [ ] 更新 `cloudbuild.yaml` 中的服務帳戶電子郵件

### 服務帳戶權限

```bash
PROJECT_ID=$(gcloud config get-value project)

# 建立服務帳戶
gcloud iam service-accounts create bakudocs-runner \
  --display-name="BakuDocs Cloud Run Service Account"

# 授予 Gemini API 權限
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:bakudocs-runner@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
```

### Cloud Build 權限

```bash
PROJECT_ID=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

# 授予 Cloud Build 部署權限
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"
```

## 🚀 部署流程

1. **推送代碼到 GitHub**:
   ```bash
   git add .
   git commit -m "Configure for Cloud Run"
   git push origin main
   ```

2. **自動觸發**:
   - Cloud Build 自動啟動
   - 構建 Docker 映像
   - 部署到 Cloud Run

3. **驗證部署**:
   - 檢查 Cloud Build 狀態
   - 檢查 Cloud Run 服務
   - 測試應用端點

## 📝 重要說明

### Gemini API 認證

✅ **無需 API key 文件** - 應用會自動使用 Cloud Run 的服務帳戶憑證

✅ **自動認證** - 在 Cloud Run 上運行時，`google.auth.default()` 會自動使用服務帳戶

✅ **本地開發** - 仍可使用 `GOOGLE_APPLICATION_CREDENTIALS` 環境變數指向本地憑證文件

### 無狀態限制

⚠️ **文件上傳** - Cloud Run 是無狀態的，上傳的文件不會持久化
- 建議後續遷移到 Cloud Storage

⚠️ **數據庫** - SQLite 文件不會持久化
- 建議後續遷移到 Cloud SQL

⚠️ **日誌** - 應用日誌會自動發送到 Cloud Logging，無需額外配置

## 📚 相關文檔

- `GITHUB_DEPLOYMENT.md` - 詳細的 GitHub 部署指南
- `GITHUB_DEPLOYMENT_QUICK.md` - 快速參考
- `CLOUD_RUN_DEPLOYMENT.md` - Cloud Run 部署指南
- `cloudbuild.yaml` - Cloud Build 配置文件

## 🔧 故障排除

### 問題：Gemini API 認證失敗

**解決方案**:
1. 確認服務帳戶有 `roles/aiplatform.user` 權限
2. 確認 Cloud Run 服務使用正確的服務帳戶
3. 檢查 Cloud Logging 中的錯誤日誌

### 問題：構建失敗

**解決方案**:
1. 檢查 `cloudbuild.yaml` 語法
2. 確認 Dockerfile 正確
3. 檢查 Cloud Build 日誌

### 問題：部署失敗

**解決方案**:
1. 確認 Cloud Build 服務帳戶有部署權限
2. 檢查 Cloud Run 日誌
3. 確認端口配置正確（8080）

## ✨ 後續改進建議

1. **文件存儲**: 遷移到 Cloud Storage
2. **數據庫**: 遷移到 Cloud SQL
3. **監控**: 設置 Cloud Monitoring 告警
4. **CDN**: 配置 Cloud CDN 加速靜態資源
5. **認證**: 配置 Cloud Run IAM 或 Firebase Authentication
