# BakuDocs Docker Quick Reference

[English](#english) | [中文](#中文)

---

## English

### 🚀 One-Click Deployment
```bash
./setup_docker.sh
```

### 📋 Basic Commands

#### Start Services
```bash
# Development environment
docker-compose up -d

# Production environment
docker-compose -f docker-compose.prod.yml up -d

# With nginx reverse proxy
docker-compose -f docker-compose.prod.yml --profile nginx up -d
```

#### Check Status
```bash
# Container status
docker-compose ps

# Application logs
docker-compose logs -f bakudocs

# Resource usage
docker stats bakudocs-app

# Health check
curl http://localhost:5001/login
```

#### Maintenance Operations
```bash
# Stop services
docker-compose down

# Restart services
docker-compose restart

# Update application
docker-compose pull && docker-compose up -d --build

# Clean up resources
docker system prune -f
```

### 📁 Important Files

| File | Purpose |
|------|---------|
| `Dockerfile` | Container image definition |
| `docker-compose.yml` | Development environment configuration |
| `docker-compose.prod.yml` | Production environment configuration |
| `setup_docker.sh` | Automated installation script |
| `DOCKER_DEPLOYMENT.md` | Detailed deployment guide |

### 🔧 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `production` | Flask environment |
| `HOST` | `0.0.0.0` | Bind host |
| `PORT` | `5001` | Application port |
| `GOOGLE_APPLICATION_CREDENTIALS` | `/app/fileanalyzer-*.json` | Google service account |

### 📂 Data Directories

| Directory | Purpose |
|-----------|---------|
| `data/uploads` | Uploaded files and analysis results |
| `data/logs` | Application logs |
| `data/databases` | SQLite database files |

### 🚨 Troubleshooting

#### Container Won't Start
```bash
docker-compose logs bakudocs
```

#### Port Already in Use
```bash
lsof -i :5001
```

#### Permission Issues
```bash
sudo chown -R 1000:1000 data/
```

#### Google API Errors
```bash
# Check service account file
ls -la fileanalyzer-463911-e71c7f7288ad.json
```

### 📊 System Requirements

- **Docker**: ≥ 20.10
- **Docker Compose**: ≥ 2.0  
- **Memory**: ≥ 2GB (4GB recommended)
- **Storage**: ≥ 5GB
- **Network**: Internet connection required

### 🔗 Access

- **Local Development**: http://localhost:5001
- **Production**: http://your-domain.com (after configuration)

---

## 中文

# BakuDocs Docker 快速參考

## 🚀 一鍵部署
```bash
./setup_docker.sh
```

## 📋 基本命令

### 啟動服務
```bash
# 開發環境
docker-compose up -d

# 生產環境
docker-compose -f docker-compose.prod.yml up -d

# 帶 nginx 反向代理
docker-compose -f docker-compose.prod.yml --profile nginx up -d
```

### 檢查狀態
```bash
# 容器狀態
docker-compose ps

# 應用日誌
docker-compose logs -f bakudocs

# 資源使用
docker stats bakudocs-app

# 健康檢查
curl http://localhost:5001/login
```

### 維護操作
```bash
# 停止服務
docker-compose down

# 重啟服務
docker-compose restart

# 更新應用
docker-compose pull && docker-compose up -d --build

# 清理資源
docker system prune -f
```

## 📁 重要文件

| 文件 | 用途 |
|------|------|
| `Dockerfile` | 容器映像定義 |
| `docker-compose.yml` | 開發環境配置 |
| `docker-compose.prod.yml` | 生產環境配置 |
| `setup_docker.sh` | 自動化安裝腳本 |
| `DOCKER_DEPLOYMENT.md` | 詳細部署指南 |

## 🔧 環境變數

| 變數 | 預設值 | 說明 |
|------|--------|------|
| `FLASK_ENV` | `production` | Flask 環境 |
| `HOST` | `0.0.0.0` | 綁定主機 |
| `PORT` | `5001` | 應用端口 |
| `GOOGLE_APPLICATION_CREDENTIALS` | `/app/fileanalyzer-*.json` | Google 服務帳號 |

## 📂 資料目錄

| 目錄 | 用途 |
|------|------|
| `data/uploads` | 上傳文件和分析結果 |
| `data/logs` | 應用程式日誌 |
| `data/databases` | SQLite 資料庫文件 |

## 🚨 故障排除

### 容器無法啟動
```bash
docker-compose logs bakudocs
```

### 端口被占用
```bash
lsof -i :5001
```

### 權限問題
```bash
sudo chown -R 1000:1000 data/
```

### Google API 錯誤
```bash
# 檢查服務帳號文件
ls -la fileanalyzer-463911-e71c7f7288ad.json
```

## 📊 系統需求

- **Docker**: ≥ 20.10
- **Docker Compose**: ≥ 2.0  
- **記憶體**: ≥ 2GB (建議 4GB)
- **儲存**: ≥ 5GB
- **網路**: 需要網路連線

## 🔗 訪問方式

- **本地開發**: http://localhost:5001
- **生產環境**: http://your-domain.com (配置後)

---

*快速參考卡 - 完整文檔請參閱 `DOCKER_DEPLOYMENT.md`*
