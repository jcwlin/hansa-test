# GitHub 部署快速參考

## 快速設置步驟

### 1. 在 Cloud Console 中連接 GitHub

1. 前往 [Cloud Build 觸發器](https://console.cloud.google.com/cloud-build/triggers)
2. 點擊「建立觸發器」
3. 選擇「GitHub (Cloud Build GitHub App)」
4. 授權並選擇倉庫
5. 配置：
   - **名稱**: `deploy-bakudocs`
   - **事件**: Push to a branch
   - **分支**: `^main$` 或 `^master$`
   - **配置類型**: Cloud Build 配置文件
   - **位置**: `hansa-test/cloudbuild.yaml`

### 2. 設置服務帳戶

```bash
PROJECT_ID=$(gcloud config get-value project)

# 建立服務帳戶（如果尚未建立）
gcloud iam service-accounts create bakudocs-runner \
  --display-name="BakuDocs Cloud Run Service Account"

# 授予 Gemini API 權限
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:bakudocs-runner@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
```

### 3. 更新 cloudbuild.yaml 中的服務帳戶

編輯 `cloudbuild.yaml`，將最後一行的 `_SERVICE_ACCOUNT_EMAIL` 替換為：
```yaml
_SERVICE_ACCOUNT_EMAIL: 'bakudocs-runner@${PROJECT_ID}.iam.gserviceaccount.com'
```

或在 Cloud Console 觸發器設定中配置替代變數。

### 4. 推送代碼

```bash
git add .
git commit -m "Configure for Cloud Run deployment"
git push origin main
```

## 重要說明

✅ **Gemini API 認證**: 應用已自動使用 Cloud Run 的默認憑證，無需 API key 文件  
✅ **自動部署**: 推送代碼到 GitHub 會自動觸發部署  
✅ **無狀態**: Cloud Run 是無狀態的，文件上傳需要使用 Cloud Storage（後續改進）

## 查看部署狀態

- Cloud Build: https://console.cloud.google.com/cloud-build/builds
- Cloud Run: https://console.cloud.google.com/run

