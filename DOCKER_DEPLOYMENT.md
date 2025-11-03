# BakuDocs Docker 部署指南

[English](#english) | [中文](#中文)

---

## English

### Docker Deployment Guide

This guide helps you deploy BakuDocs using Docker for easy, consistent deployment across different environments.

### Prerequisites

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher (included with Docker Desktop)
- **System Requirements**: 
  - Memory: Minimum 2GB RAM (4GB recommended)
  - Storage: At least 5GB free disk space
  - Network: Internet access for downloading dependencies and Google API calls

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd BakuDocs
   ```

2. **Prepare data directories**:
   ```bash
   mkdir -p data/{uploads,logs,databases}
   ```

3. **Configure Google Service Account**:
   - Ensure your `fileanalyzer-463911-e71c7f7288ad.json` file is in the project root
   - Or update the path in `docker-compose.yml`

4. **Build and start**:
   ```bash
   docker-compose up -d
   ```

5. **Access the application**:
   - Open your browser and navigate to `http://localhost:5001`
   - Default admin credentials may need to be configured on first run

### Configuration

#### Environment Variables

You can customize the deployment by modifying environment variables in `docker-compose.yml`:

- `FLASK_ENV`: Set to `production` for production deployment
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to Google service account JSON file
- `PORT`: Application port (default: 5001)
- `HOST`: Bind address (default: 0.0.0.0 for production)

#### Persistent Data

The following directories are mounted as volumes for data persistence:

- `./data/uploads`: Uploaded files and analysis results
- `./data/logs`: Application logs
- `./data/databases`: SQLite databases and history files

### Production Deployment

For production environments, consider these additional steps:

1. **Use a reverse proxy** (nginx/Apache) for SSL termination and load balancing

2. **Set up monitoring**:
   ```bash
   # Check container status
   docker-compose ps
   
   # View logs
   docker-compose logs -f bakudocs
   
   # Check resource usage
   docker stats bakudocs-app
   ```

3. **Backup important data**:
   ```bash
   # Backup data directory
   tar -czf bakudocs-backup-$(date +%Y%m%d).tar.gz data/
   ```

4. **Update the application**:
   ```bash
   docker-compose pull
   docker-compose up -d --build
   ```

### Troubleshooting

#### Common Issues

1. **Container fails to start**:
   ```bash
   # Check logs
   docker-compose logs bakudocs
   
   # Check if port is already in use
   lsof -i :5001
   ```

2. **Google API authentication errors**:
   - Verify the service account JSON file exists and has correct permissions
   - Check if the file path in docker-compose.yml is correct

3. **OCR not working**:
   - The Docker image includes Tesseract OCR with English and Chinese support
   - Check if additional language packs are needed

4. **Permission issues**:
   ```bash
   # Fix permissions for data directories
   sudo chown -R 1000:1000 data/
   ```

### Scaling

For high-traffic deployments:

1. **Use Docker Swarm or Kubernetes** for orchestration
2. **Add a load balancer** for multiple instances
3. **Use external databases** (PostgreSQL/MySQL) instead of SQLite
4. **Implement caching** with Redis for session management

---

## 中文

### Docker 部署指南

本指南幫助您使用 Docker 部署 BakuDocs，實現跨環境的簡單、一致部署。

### 前置需求

- **Docker**: 版本 20.10 或更高
- **Docker Compose**: 版本 2.0 或更高（Docker Desktop 已包含）
- **系統需求**:
  - 記憶體：最少 2GB RAM（建議 4GB）
  - 儲存空間：至少 5GB 可用磁碟空間
  - 網路：需要網路連線以下載依賴項和呼叫 Google API

### 快速開始

1. **複製專案**:
   ```bash
   git clone <repository-url>
   cd BakuDocs
   ```

2. **準備資料目錄**:
   ```bash
   mkdir -p data/{uploads,logs,databases}
   ```

3. **設定 Google 服務帳號**:
   - 確保您的 `fileanalyzer-463911-e71c7f7288ad.json` 檔案在專案根目錄
   - 或更新 `docker-compose.yml` 中的路徑

4. **建置並啟動**:
   ```bash
   docker-compose up -d
   ```

5. **存取應用程式**:
   - 開啟瀏覽器並訪問 `http://localhost:5001`
   - 首次執行時可能需要設定預設管理員憑證

### 設定

#### 環境變數

您可以透過修改 `docker-compose.yml` 中的環境變數來自訂部署：

- `FLASK_ENV`: 生產環境設為 `production`
- `GOOGLE_APPLICATION_CREDENTIALS`: Google 服務帳號 JSON 檔案路徑
- `PORT`: 應用程式埠號（預設：5001）
- `HOST`: 綁定位址（生產環境預設：0.0.0.0）

#### 持久化資料

以下目錄掛載為卷宗以實現資料持久化：

- `./data/uploads`: 上傳檔案和分析結果
- `./data/logs`: 應用程式日誌
- `./data/databases`: SQLite 資料庫和歷史檔案

### 生產環境部署

對於生產環境，建議考慮以下額外步驟：

1. **使用反向代理**（nginx/Apache）進行 SSL 終止和負載平衡

2. **設定監控**:
   ```bash
   # 檢查容器狀態
   docker-compose ps
   
   # 檢視日誌
   docker-compose logs -f bakudocs
   
   # 檢查資源使用情況
   docker stats bakudocs-app
   ```

3. **備份重要資料**:
   ```bash
   # 備份資料目錄
   tar -czf bakudocs-backup-$(date +%Y%m%d).tar.gz data/
   ```

4. **更新應用程式**:
   ```bash
   docker-compose pull
   docker-compose up -d --build
   ```

### 故障排除

#### 常見問題

1. **容器啟動失敗**:
   ```bash
   # 檢查日誌
   docker-compose logs bakudocs
   
   # 檢查埠號是否已被使用
   lsof -i :5001
   ```

2. **Google API 認證錯誤**:
   - 驗證服務帳號 JSON 檔案存在且具有正確權限
   - 檢查 docker-compose.yml 中的檔案路徑是否正確

3. **OCR 無法運作**:
   - Docker 映像檔包含 Tesseract OCR 及英文和中文支援
   - 檢查是否需要額外的語言包

4. **權限問題**:
   ```bash
   # 修復資料目錄權限
   sudo chown -R 1000:1000 data/
   ```

### 擴展

對於高流量部署：

1. **使用 Docker Swarm 或 Kubernetes** 進行編排
2. **添加負載平衡器** 支援多個實例
3. **使用外部資料庫**（PostgreSQL/MySQL）取代 SQLite
4. **實作快取**，使用 Redis 進行會話管理
