# GitHub 部署到 Cloud Run 指南

## 概述

本指南說明如何配置 GitHub 倉庫，讓 Google Cloud Run 可以自動從 GitHub 部署應用。

## 前置需求

1. ✅ Google Cloud 專案已建立
2. ✅ Cloud Build API 已啟用
3. ✅ Cloud Run API 已啟用
4. ✅ GitHub 倉庫已建立

## 配置步驟

### 1. 設置 Cloud Build 服務帳戶權限

```bash
# 獲取專案編號
PROJECT_ID=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

# 授予 Cloud Build 服務帳戶必要的權限
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

# 授予 Cloud Build 服務帳戶 Cloud Storage 權限（用於推送映像）
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
  --role="roles/storage.admin"
```

### 2. 連接 GitHub 倉庫到 Cloud Build

#### 方法 A: 使用 Cloud Console（推薦）

1. 前往 [Cloud Build 觸發器頁面](https://console.cloud.google.com/cloud-build/triggers)
2. 點擊「建立觸發器」
3. 選擇「GitHub (Cloud Build GitHub App)」
4. 授權 Cloud Build 存取您的 GitHub 帳戶
5. 選擇倉庫和分支（通常是 `main` 或 `master`）
6. 配置觸發器：
   - **名稱**: `deploy-bakudocs`
   - **事件**: Push to a branch
   - **分支**: `^main$` (或 `^master$`)
   - **配置類型**: Cloud Build 配置文件
   - **位置**: `hansa-test/cloudbuild.yaml`

#### 方法 B: 使用 gcloud CLI

```bash
gcloud builds triggers create github \
  --name="deploy-bakudocs" \
  --repo-name="YOUR_GITHUB_REPO" \
  --repo-owner="YOUR_GITHUB_USERNAME" \
  --branch-pattern="^main$" \
  --build-config="hansa-test/cloudbuild.yaml" \
  --region="asia-east1"
```

### 3. 配置 Cloud Run 服務帳戶

Cloud Run 需要使用具有 Gemini API 權限的服務帳戶：

```bash
# 建立服務帳戶（如果尚未建立）
gcloud iam service-accounts create bakudocs-runner \
  --display-name="BakuDocs Cloud Run Service Account"

# 授予 Gemini API 權限
PROJECT_ID=$(gcloud config get-value project)
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:bakudocs-runner@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

# 授予其他必要的權限
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:bakudocs-runner@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/run.invoker"
```

### 4. 更新 cloudbuild.yaml 中的服務帳戶

編輯 `cloudbuild.yaml`，將 `_SERVICE_ACCOUNT_EMAIL` 替換為您的服務帳戶：

```yaml
substitutions:
  _SERVICE_ACCOUNT_EMAIL: 'bakudocs-runner@${PROJECT_ID}.iam.gserviceaccount.com'
```

或在 Cloud Console 中配置：
1. 前往 Cloud Build 觸發器
2. 編輯觸發器
3. 在「替代變數」中添加：
   - 變數名稱: `_SERVICE_ACCOUNT_EMAIL`
   - 值: `bakudocs-runner@YOUR_PROJECT_ID.iam.gserviceaccount.com`

### 5. 推送代碼到 GitHub

```bash
git add .
git commit -m "Configure for Cloud Run deployment"
git push origin main
```

### 6. 驗證部署

部署完成後，您可以在以下位置查看：

- **Cloud Build 歷史**: https://console.cloud.google.com/cloud-build/builds
- **Cloud Run 服務**: https://console.cloud.google.com/run

## 重要配置說明

### ✅ Gemini API 認證

應用已配置為自動使用 Cloud Run 的**默認憑證**，無需手動設置 API key：

- 在 Cloud Run 上運行時，會自動使用服務帳戶的憑證
- 不需要在 Docker 映像中包含 JSON 憑證文件
- 確保 Cloud Run 服務帳戶有 `roles/aiplatform.user` 權限

### ✅ 環境變數

Cloud Run 會自動設置以下環境變數：
- `PORT`: 自動設置為 8080
- `FLASK_ENV`: 透過 cloudbuild.yaml 設置為 `production`

### ✅ 監控和日誌

- 應用日誌會自動發送到 Cloud Logging
- 可以在 Cloud Console 中查看日誌
- 無需配置額外的日誌服務

## 故障排除

### 問題：構建失敗

檢查 Cloud Build 日誌：
```bash
gcloud builds list --limit=5
gcloud builds log [BUILD_ID]
```

### 問題：部署失敗

檢查 Cloud Run 日誌：
```bash
gcloud run services logs read bakudocs --limit=50
```

### 問題：Gemini API 認證失敗

確保服務帳戶有正確的權限：
```bash
gcloud projects get-iam-policy YOUR_PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:bakudocs-runner@*"
```

### 問題：端口錯誤

確保應用監聽 `0.0.0.0` 和環境變數 `PORT`（已在 Dockerfile 中配置）

## 自動部署流程

當您推送代碼到 GitHub 時：

1. ✅ Cloud Build 觸發器自動啟動
2. ✅ 使用 `cloudbuild.yaml` 構建 Docker 映像
3. ✅ 推送映像到 Container Registry
4. ✅ 自動部署到 Cloud Run
5. ✅ 新版本立即生效

## 手動部署

如果需要手動觸發部署：

```bash
cd hansa-test
gcloud builds submit --config cloudbuild.yaml
```

## 後續改進

1. **設置環境變數**: 在 Cloud Run 控制台中設置其他環境變數
2. **配置自定義域名**: 設置 Cloud Run 的自定義域名
3. **設置 CI/CD 規則**: 配置只在特定分支或標籤時部署
4. **監控和告警**: 設置 Cloud Monitoring 告警

