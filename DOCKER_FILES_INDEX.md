# BakuDocs Docker Files Index

[English](#english) | [中文](#中文)

---

## English

This document lists all Docker deployment-related files in the BakuDocs project and their purposes.

### 📁 Core Docker Files

#### 1. `Dockerfile`
- **Purpose**: Defines the BakuDocs application container image
- **Contains**: 
  - Python 3.11-slim base image
  - System dependencies installation (Tesseract OCR, Poppler, etc.)
  - Python dependencies installation
  - Application code copying
  - Security settings (non-root user)
  - Health check configuration

#### 2. `docker-compose.yml`
- **Purpose**: Docker Compose configuration for development environment
- **Features**:
  - Exposes port 5001
  - Mounts local data directories
  - Development-friendly settings
  - Restart policy: unless-stopped

#### 3. `docker-compose.prod.yml`
- **Purpose**: Docker Compose configuration for production environment
- **Features**:
  - Production-grade resource limits
  - Named volumes for data persistence
  - Log rotation configuration
  - Optional nginx reverse proxy
  - Strict restart policy

#### 4. `docker-compose.podman.yml`
- **Purpose**: Podman-optimized Docker Compose configuration
- **Features**:
  - SELinux-compatible volume mounts (:Z)
  - Podman-specific labels and environment variables
  - Better permission handling with PODMAN_USERNS=keep-id
  - Full compatibility with both Podman and Docker

#### 5. `.dockerignore`
- **Purpose**: Specifies files to exclude when building Docker images
- **Excludes**:
  - Git files and cache
  - Python cache and compiled files
  - Development files and temporary files
  - Large data files

### 📚 Documentation and Scripts

#### 5. `DOCKER_DEPLOYMENT.md`
- **Purpose**: Complete Docker deployment guide (bilingual)
- **Content**:
  - System requirements and prerequisites
  - Detailed deployment steps
  - Configuration options explanation
  - Production environment best practices
  - Troubleshooting guide
  - Monitoring and maintenance instructions

#### 6. `DEPLOYMENT_SUMMARY.md`
- **Purpose**: Complete record and summary of deployment process
- **Content**:
  - Technical specifications record
  - Detailed deployment process steps
  - Security implementation record
  - Monitoring and maintenance guide
  - Version history and future plans

#### 7. `DOCKER_QUICK_REFERENCE.md`
- **Purpose**: Quick reference for common Docker commands
- **Content**:
  - One-click deployment commands
  - Basic operation commands
  - Troubleshooting commands
  - System requirements summary

#### 8. `DOCKER_FILES_INDEX.md`
- **Purpose**: This document, index of all Docker-related files

### 🔧 Automation Scripts

#### 9. `setup_docker.sh`
- **Purpose**: Automated Docker environment setup script
- **Functions**:
  - Check Docker and Docker Compose installation
  - Create necessary data directories
  - Validate configuration files
  - Automatically build and start containers
  - Provide status checks and next steps guidance

#### 10. `setup_podman.sh`
- **Purpose**: Automated Podman environment setup script
- **Functions**:
  - Check Podman installation and version
  - Handle Podman machine setup (macOS/Windows)
  - Support both podman-compose and docker-compose
  - Use Podman-optimized compose configuration
  - Provide Podman-specific commands and guidance

### 🔄 Modified Application Files

#### 11. `app.py` (Modified sections)
- **Modifications**: Added production environment support
- **New features**:
  - Environment variables support (FLASK_ENV, HOST, PORT)
  - Production environment optimization configuration
  - Docker-friendly startup logic

### 📝 Updated Documentation

#### 12. `PODMAN_DEPLOYMENT.md`
- **Purpose**: Complete Podman deployment guide (bilingual)
- **Content**:
  - Podman introduction and advantages
  - Installation instructions for different platforms
  - Podman-specific optimizations and features
  - Migration guide from Docker
  - Troubleshooting and best practices

#### 11. `README.md` (Updated sections)
- **New content**: Docker quick start section
- **Improvements**:
  - Added Docker deployment option before main installation guide
  - Provided one-click deployment commands
  - Referenced detailed deployment documentation

### 🎯 File Usage Guide

#### Quick Start for New Users
1. Read the Docker quick start section in `README.md`
2. Run `./setup_docker.sh` for one-click deployment
3. Refer to `DOCKER_QUICK_REFERENCE.md` for common commands

#### Detailed Deployment
1. Read `DOCKER_DEPLOYMENT.md` for complete deployment process
2. Choose appropriate `docker-compose.yml` file based on environment
3. Refer to `DEPLOYMENT_SUMMARY.md` for technical details

#### Troubleshooting
1. Check troubleshooting section in `DOCKER_QUICK_REFERENCE.md`
2. Refer to detailed troubleshooting guide in `DOCKER_DEPLOYMENT.md`
3. Check container logs and status

#### Production Environment Deployment
1. Use `docker-compose.prod.yml` configuration
2. Follow production environment best practices in `DOCKER_DEPLOYMENT.md`
3. Implement monitoring and maintenance recommendations from `DEPLOYMENT_SUMMARY.md`

### 📊 File Relationship Diagram

```
README.md (Entry point)
    ↓
DOCKER_QUICK_REFERENCE.md (Quick start)
    ↓
DOCKER_DEPLOYMENT.md (Detailed guide)
    ↓
DEPLOYMENT_SUMMARY.md (Complete record)
    ↓
setup_docker.sh (Automated execution)
    ↓
docker-compose.yml / docker-compose.prod.yml (Environment configuration)
    ↓
Dockerfile (Container definition)
```

---

## 中文

# BakuDocs Docker 文件索引

本文件列出了 BakuDocs 專案中所有與 Docker 部署相關的文件及其用途。

## 📁 核心 Docker 文件

### 1. `Dockerfile`
- **用途**: 定義 BakuDocs 應用程式的容器映像
- **包含**: 
  - Python 3.11-slim 基礎映像
  - 系統依賴項安裝（Tesseract OCR、Poppler等）
  - Python 依賴項安裝
  - 應用程式代碼複製
  - 安全設定（非 root 使用者）
  - 健康檢查配置

### 2. `docker-compose.yml`
- **用途**: 開發環境的 Docker Compose 配置
- **特點**:
  - 暴露端口 5001
  - 掛載本地資料目錄
  - 開發友好的設定
  - 重啟策略：unless-stopped

### 3. `docker-compose.prod.yml`
- **用途**: 生產環境的 Docker Compose 配置
- **特點**:
  - 生產級資源限制
  - 命名卷宗用於資料持久化
  - 日誌輪轉配置
  - 可選的 nginx 反向代理
  - 嚴格的重啟策略

### 4. `docker-compose.podman.yml`
- **用途**: Podman 優化的 Docker Compose 配置
- **特點**:
  - SELinux 兼容的卷宗掛載（:Z）
  - Podman 特定的標籤和環境變數
  - 使用 PODMAN_USERNS=keep-id 的更好權限處理
  - 與 Podman 和 Docker 完全兼容

### 5. `.dockerignore`
- **用途**: 指定建置 Docker 映像時要排除的文件
- **排除內容**:
  - Git 文件和快取
  - Python 快取和編譯文件
  - 開發文件和臨時文件
  - 大型資料文件

## 📚 部署文檔

### 5. `DOCKER_DEPLOYMENT.md`
- **用途**: 完整的 Docker 部署指南（中英文）
- **內容**:
  - 系統需求和前置條件
  - 詳細部署步驟
  - 配置選項說明
  - 生產環境最佳實踐
  - 故障排除指南
  - 監控和維護說明

### 6. `DEPLOYMENT_SUMMARY.md`
- **用途**: 部署過程的完整記錄和總結
- **內容**:
  - 技術規格記錄
  - 部署流程詳細步驟
  - 安全性實施記錄
  - 監控和維護指南
  - 版本歷史和未來計劃

### 7. `DOCKER_QUICK_REFERENCE.md`
- **用途**: 常用 Docker 命令快速參考
- **內容**:
  - 一鍵部署命令
  - 基本操作命令
  - 故障排除命令
  - 系統需求摘要

### 8. `DOCKER_FILES_INDEX.md`
- **用途**: 本文件，所有 Docker 相關文件的索引

### 9. `PODMAN_DEPLOYMENT.md`
- **用途**: 完整的 Podman 部署指南（中英文）
- **內容**:
  - Podman 介紹和優勢
  - 不同平台的安裝說明
  - Podman 特定的優化和功能
  - 從 Docker 遷移的指南
  - 故障排除和最佳實踐

## 🔧 自動化腳本

### 10. `setup_docker.sh`
- **用途**: 自動化 Docker 環境設置腳本
- **功能**:
  - 檢查 Docker 和 Docker Compose 安裝
  - 創建必要的資料目錄
  - 驗證配置文件
  - 自動建置和啟動容器
  - 提供狀態檢查和後續步驟指引

### 11. `setup_podman.sh`
- **用途**: 自動化 Podman 環境設置腳本
- **功能**:
  - 檢查 Podman 安裝和版本
  - 處理 Podman machine 設置（macOS/Windows）
  - 支援 podman-compose 和 docker-compose
  - 使用 Podman 優化的 compose 配置
  - 提供 Podman 特定的命令和指引

## 🔄 修改的應用文件

### 12. `app.py` (修改部分)
- **修改內容**: 添加生產環境支援
- **新增功能**:
  - 環境變數支援（FLASK_ENV、HOST、PORT）
  - 生產環境優化配置
  - Docker 友好的啟動邏輯

## 📝 更新的文檔

### 13. `README.md` (更新部分)
- **新增內容**: Docker 快速開始部分
- **改進**:
  - 在主要安裝指南前添加 Docker 部署選項
  - 提供一鍵部署命令
  - 引用詳細部署文檔

## 🎯 文件使用指南

### 新用戶快速開始
1. 閱讀 `README.md` 中的 Docker 快速開始部分
2. 運行 `./setup_docker.sh` 進行一鍵部署
3. 參考 `DOCKER_QUICK_REFERENCE.md` 了解常用命令

### 詳細部署
1. 閱讀 `DOCKER_DEPLOYMENT.md` 了解完整部署流程
2. 根據環境選擇適當的 `docker-compose.yml` 文件
3. 參考 `DEPLOYMENT_SUMMARY.md` 了解技術細節

### 故障排除
1. 查看 `DOCKER_QUICK_REFERENCE.md` 中的故障排除部分
2. 參考 `DOCKER_DEPLOYMENT.md` 中的詳細故障排除指南
3. 檢查容器日誌和狀態

### 生產環境部署
1. 使用 `docker-compose.prod.yml` 配置
2. 遵循 `DOCKER_DEPLOYMENT.md` 中的生產環境最佳實踐
3. 實施 `DEPLOYMENT_SUMMARY.md` 中的監控和維護建議

## 📊 文件關係圖

```
README.md (入口點)
    ↓
DOCKER_QUICK_REFERENCE.md (快速開始)
    ↓
DOCKER_DEPLOYMENT.md (詳細指南) ←→ PODMAN_DEPLOYMENT.md (Podman 指南)
    ↓
DEPLOYMENT_SUMMARY.md (完整記錄)
    ↓
setup_docker.sh (Docker 自動化) ←→ setup_podman.sh (Podman 自動化)
    ↓
docker-compose.yml / docker-compose.prod.yml / docker-compose.podman.yml (環境配置)
    ↓
Dockerfile (容器定義)
```

---

*此索引確保所有 Docker 和 Podman 部署相關的文件都有清楚的記錄和用途說明，便於團隊成員和新用戶快速找到所需資源。*

## 🆕 Podman 支援摘要

### 新增的 Podman 文件
- **`docker-compose.podman.yml`**: Podman 優化的 compose 配置
- **`setup_podman.sh`**: Podman 專用設置腳本
- **`PODMAN_DEPLOYMENT.md`**: 完整的 Podman 部署指南

### Podman 優勢
- **無守護進程架構**: 更低的資源使用
- **更好的安全性**: 無根容器執行
- **Docker 完全兼容**: 無縫遷移
- **Kubernetes 就緒**: 原生支援
- **開源**: Apache 2.0 許可證

### 使用建議
- **新部署**: 推薦使用 Podman（更現代、更安全）
- **現有 Docker 環境**: 可以無縫遷移到 Podman
- **企業環境**: Podman 提供更好的安全性和資源管理
