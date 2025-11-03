# BakuDocs Podman 部署指南 / BakuDocs Podman Deployment Guide

[English](#english) | [中文](#chinese)

---

## English

### 🐳 What is Podman?

[Podman](https://podman.io/) is a daemonless container engine for developing, managing, and running containers. It's a drop-in replacement for Docker that provides:

- **Daemonless Architecture**: No background service required
- **Rootless Containers**: Better security through non-root execution
- **Docker Compatibility**: Full compatibility with Docker commands and images
- **Kubernetes Ready**: Native support for Kubernetes manifests
- **Open Source**: Apache 2.0 licensed

### ✅ Podman Compatibility

Our Docker configuration is **100% compatible** with Podman:

- ✅ Standard Dockerfile syntax
- ✅ Docker Compose support (via `docker-compose` or `podman-compose`)
- ✅ OCI-compliant container images
- ✅ Volume mounting and networking
- ✅ Environment variables and health checks

### 🚀 Quick Start with Podman

#### 1. Install Podman

**macOS:**
```bash
brew install podman
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install podman
```

**CentOS/RHEL/Fedora:**
```bash
sudo dnf install podman  # or sudo yum install podman
```

#### 2. One-Click Deployment

```bash
# Make script executable
chmod +x setup_podman.sh

# Run the setup script
./setup_podman.sh
```

#### 3. Manual Deployment

```bash
# Create data directories
mkdir -p data/{uploads,logs,databases}

# Build and start with Podman-optimized compose
docker-compose -f docker-compose.podman.yml up -d --build

# Or use podman-compose if available
podman-compose -f docker-compose.podman.yml up -d --build
```

### 🔧 Podman-Specific Optimizations

Our `docker-compose.podman.yml` includes several Podman optimizations:

#### Volume Mounting
```yaml
volumes:
  - ./data/uploads:/app/uploads:Z    # :Z for SELinux compatibility
  - ./config.yaml:/app/config.yaml:Z
```

#### Podman Labels
```yaml
labels:
  - "io.podman.autoupdate=registry"
  - "org.opencontainers.image.description=BakuDocs Smart Document Analysis System"
```

#### User Namespace
```yaml
environment:
  - PODMAN_USERNS=keep-id  # Better permission handling
```

### 📱 Podman Desktop

For GUI users, [Podman Desktop](https://podman.io/desktop/) provides a user-friendly interface:

1. **Install Podman Desktop** from [podman.io/desktop](https://podman.io/desktop/)
2. **Import our compose file**: `docker-compose.podman.yml`
3. **Start containers** with one click
4. **Monitor logs** and container status visually

### 🐧 Linux Systemd Integration

On Linux systems, Podman can integrate with systemd for automatic startup:

```bash
# Generate systemd service files
podman generate systemd --name bakudocs-app --files

# Enable and start the service
sudo systemctl enable container-bakudocs-app
sudo systemctl start container-bakudocs-app
```

### 🔍 Troubleshooting

#### Common Issues

**Permission Denied:**
```bash
# Fix volume permissions
sudo chown -R $USER:$USER data/
```

**Port Already in Use:**
```bash
# Check what's using port 5001
sudo lsof -i :5001

# Stop conflicting service
sudo systemctl stop conflicting-service
```

**Podman Machine Issues (macOS/Windows):**
```bash
# Restart Podman machine
podman machine stop
podman machine start

# Check machine status
podman machine list
```

#### Logs and Debugging

```bash
# View container logs
podman logs bakudocs-app

# Execute commands in container
podman exec -it bakudocs-app /bin/bash

# Inspect container
podman inspect bakudocs-app
```

### 📊 Performance Benefits

Podman offers several advantages over Docker:

- **Lower Resource Usage**: No daemon process
- **Better Security**: Rootless execution
- **Faster Startup**: No background service initialization
- **System Integration**: Native systemd support on Linux

### 🔄 Migration from Docker

If you're currently using Docker:

1. **Stop Docker containers:**
   ```bash
   docker-compose down
   ```

2. **Install Podman:**
   ```bash
   # See installation instructions above
   ```

3. **Use Podman-optimized compose:**
   ```bash
   docker-compose -f docker-compose.podman.yml up -d
   ```

4. **Verify migration:**
   ```bash
   podman ps
   ```

---

## Chinese

### 🐳 什麼是 Podman？

[Podman](https://podman.io/) 是一個無守護進程的容器引擎，用於開發、管理和運行容器。它是 Docker 的替代品，提供：

- **無守護進程架構**：無需背景服務
- **無根容器**：通過非根執行提供更好的安全性
- **Docker 兼容性**：完全兼容 Docker 命令和鏡像
- **Kubernetes 就緒**：原生支持 Kubernetes 清單
- **開源**：Apache 2.0 許可證

### ✅ Podman 兼容性

我們的 Docker 配置與 Podman **100% 兼容**：

- ✅ 標準 Dockerfile 語法
- ✅ Docker Compose 支持（通過 `docker-compose` 或 `podman-compose`）
- ✅ OCI 兼容的容器鏡像
- ✅ 卷掛載和網絡
- ✅ 環境變量和健康檢查

### 🚀 使用 Podman 快速開始

#### 1. 安裝 Podman

**macOS:**
```bash
brew install podman
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install podman
```

**CentOS/RHEL/Fedora:**
```bash
sudo dnf install podman  # 或 sudo yum install podman
```

#### 2. 一鍵部署

```bash
# 使腳本可執行
chmod +x setup_podman.sh

# 運行設置腳本
./setup_podman.sh
```

#### 3. 手動部署

```bash
# 創建數據目錄
mkdir -p data/{uploads,logs,databases}

# 使用 Podman 優化的 compose 構建和啟動
docker-compose -f docker-compose.podman.yml up -d --build

# 或使用 podman-compose（如果可用）
podman-compose -f docker-compose.podman.yml up -d --build
```

### 🔧 Podman 特定優化

我們的 `docker-compose.podman.yml` 包含幾個 Podman 優化：

#### 卷掛載
```yaml
volumes:
  - ./data/uploads:/app/uploads:Z    # :Z 用於 SELinux 兼容性
  - ./config.yaml:/app/config.yaml:Z
```

#### Podman 標籤
```yaml
labels:
  - "io.podman.autoupdate=registry"
  - "org.opencontainers.image.description=BakuDocs Smart Document Analysis System"
```

#### 用戶命名空間
```yaml
environment:
  - PODMAN_USERNS=keep-id  # 更好的權限處理
```

### 📱 Podman Desktop

對於 GUI 用戶，[Podman Desktop](https://podman.io/desktop/) 提供用戶友好的界面：

1. 從 [podman.io/desktop](https://podman.io/desktop/) **安裝 Podman Desktop**
2. **導入我們的 compose 文件**：`docker-compose.podman.yml`
3. **一鍵啟動容器**
4. **視覺化監控日誌**和容器狀態

### 🐧 Linux Systemd 集成

在 Linux 系統上，Podman 可以與 systemd 集成以實現自動啟動：

```bash
# 生成 systemd 服務文件
podman generate systemd --name bakudocs-app --files

# 啟用並啟動服務
sudo systemctl enable container-bakudocs-app
sudo systemctl start container-bakudocs-app
```

### 🔍 故障排除

#### 常見問題

**權限被拒絕：**
```bash
# 修復卷權限
sudo chown -R $USER:$USER data/
```

**端口已被使用：**
```bash
# 檢查什麼在使用端口 5001
sudo lsof -i :5001

# 停止衝突的服務
sudo systemctl stop conflicting-service
```

**Podman Machine 問題（macOS/Windows）：**
```bash
# 重啟 Podman machine
podman machine stop
podman machine start

# 檢查 machine 狀態
podman machine list
```

#### 日誌和調試

```bash
# 查看容器日誌
podman logs bakudocs-app

# 在容器中執行命令
podman exec -it bakudocs-app /bin/bash

# 檢查容器
podman inspect bakudocs-app
```

### 📊 性能優勢

Podman 相比 Docker 提供幾個優勢：

- **更低的資源使用**：無守護進程
- **更好的安全性**：無根執行
- **更快的啟動**：無背景服務初始化
- **系統集成**：Linux 上的原生 systemd 支持

### 🔄 從 Docker 遷移

如果您目前使用 Docker：

1. **停止 Docker 容器：**
   ```bash
   docker-compose down
   ```

2. **安裝 Podman：**
   ```bash
   # 參見上面的安裝說明
   ```

3. **使用 Podman 優化的 compose：**
   ```bash
   docker-compose -f docker-compose.podman.yml up -d
   ```

4. **驗證遷移：**
   ```bash
   podman ps
   ```

---

## 📚 Additional Resources / 額外資源

- [Podman Official Documentation](https://podman.io/docs)
- [Podman vs Docker Comparison](https://podman.io/what-is-podman)
- [Podman Desktop Download](https://podman.io/desktop/)
- [BakuDocs Docker Deployment Guide](DOCKER_DEPLOYMENT.md)

---

*This guide ensures that BakuDocs can be deployed seamlessly using Podman while maintaining full compatibility with Docker workflows.*
*本指南確保 BakuDocs 可以使用 Podman 無縫部署，同時保持與 Docker 工作流程的完全兼容性。*
