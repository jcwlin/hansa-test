# BakuDocs Installation Guide

[English](#english) | [中文](#中文)

---

## English

### Prerequisites

Before installing BakuDocs, ensure your system meets the following requirements:

- **Python**: Version 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Memory**: Minimum 4GB RAM (8GB recommended for large file processing)
- **Storage**: At least 2GB free disk space
- **Internet Connection**: Required for Google Gemini API access

### Step 1: System Dependencies

#### Install Tesseract OCR

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-chi-tra
```

**macOS:**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Tesseract
brew install tesseract
```

**Windows:**
1. Download Tesseract installer from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer and follow the setup wizard
3. Add Tesseract to your system PATH

#### Install Poppler (for PDF processing)

**Ubuntu/Debian:**
```bash
sudo apt-get install poppler-utils
```

**macOS:**
```bash
brew install poppler
```

**Windows:**
1. Download Poppler from [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases)
2. Extract to a folder (e.g., `C:\poppler`)
3. Add `C:\poppler\Library\bin` to your system PATH

### Step 2: Python Environment Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd bakudocs-document-analyzer
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   
   # Activate virtual environment
   # On Windows:
   .venv\Scripts\activate
   
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Upgrade pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Step 3: Google Cloud Setup

1. **Create Google Cloud Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable the Vertex AI API and Generative AI API

2. **Create Service Account:**
   - Navigate to IAM & Admin > Service Accounts
   - Click "Create Service Account"
   - Assign roles: "Vertex AI User" and "AI Platform Developer"
   - Generate and download JSON key file

3. **Configure credentials:**
   - Place the JSON key file in the project root directory
   - Update the filename in `utils_gemini.py` if different from default
   - Set environment variable (optional):
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/keyfile.json"
     ```

### Step 4: Application Configuration

1. **Edit configuration file:**
   ```bash
   cp config.yaml config.yaml.backup  # Backup original
   nano config.yaml  # Edit with your preferred editor
   ```

2. **Key configuration options:**
   ```yaml
   ocr_lang: eng  # OCR language: 'eng', 'chi_tra', 'eng+chi_tra'
   
   # Add custom analyzers if needed
   analyzers:
     Custom_Analyzer:
       enabled: true
   ```

3. **Create upload directory:**
   ```bash
   mkdir -p uploads logs
   chmod 755 uploads logs
   ```

### Step 5: Database Initialization

The application will automatically create the SQLite database on first run. Default admin credentials:
- **Username**: `admin`
- **Password**: `admin123`

**Important**: Change the default admin password after first login!

### Step 6: Start the Application

1. **Run the application:**
   ```bash
   python app.py
   ```

2. **Access the web interface:**
   - Open your browser
   - Navigate to `http://localhost:5000`
   - Login with admin credentials

### Step 7: Verification

1. **Test file upload:**
   - Upload a sample PDF or image file
   - Select an analysis type
   - Verify processing completes successfully

2. **Check logs:**
   ```bash
   tail -f logs/test_log.txt
   ```

### Troubleshooting

#### Common Issues

**1. Tesseract not found:**
```bash
# Verify Tesseract installation
tesseract --version

# If not found, check PATH or reinstall
```

**2. Google API authentication errors:**
- Verify JSON key file path and permissions
- Check API is enabled in Google Cloud Console
- Ensure service account has proper roles

**3. PDF processing errors:**
```bash
# Verify Poppler installation
pdftoppm -h

# If not found, reinstall Poppler
```

**4. Memory issues with large files:**
- Increase system memory
- Process files in smaller batches
- Adjust `MAX_CONTENT_LENGTH` in app.py

**5. Port already in use:**
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process or use different port
python app.py --port 5001
```

### Production Deployment

For production deployment, consider:

1. **Use production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Set up reverse proxy (Nginx):**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

3. **Configure SSL certificate**
4. **Set up monitoring and logging**
5. **Configure backup procedures**

---

## 中文

### 系統要求

安裝 BakuDocs 前，請確保您的系統滿足以下要求：

- **Python**: 3.8 或更高版本
- **操作系統**: Windows 10+、macOS 10.14+ 或 Linux (Ubuntu 18.04+)
- **內存**: 最少 4GB RAM（建議 8GB 用於大文件處理）
- **存儲空間**: 至少 2GB 可用磁盤空間
- **網絡連接**: 需要訪問 Google Gemini API

### 步驟 1: 系統依賴

#### 安裝 Tesseract OCR

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-chi-tra
```

**macOS:**
```bash
# 如未安裝 Homebrew，先安裝
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安裝 Tesseract
brew install tesseract
```

**Windows:**
1. 從 [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki) 下載 Tesseract 安裝程序
2. 運行安裝程序並按照設置向導操作
3. 將 Tesseract 添加到系統 PATH

#### 安裝 Poppler（用於 PDF 處理）

**Ubuntu/Debian:**
```bash
sudo apt-get install poppler-utils
```

**macOS:**
```bash
brew install poppler
```

**Windows:**
1. 從 [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases) 下載 Poppler
2. 解壓到文件夾（例如 `C:\poppler`）
3. 將 `C:\poppler\Library\bin` 添加到系統 PATH

### 步驟 2: Python 環境設置

1. **克隆倉庫:**
   ```bash
   git clone <repository-url>
   cd bakudocs-document-analyzer
   ```

2. **創建虛擬環境:**
   ```bash
   python -m venv .venv
   
   # 激活虛擬環境
   # Windows:
   .venv\Scripts\activate
   
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **升級 pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

4. **安裝 Python 依賴:**
   ```bash
   pip install -r requirements.txt
   ```

### 步驟 3: Google Cloud 設置

1. **創建 Google Cloud 項目:**
   - 前往 [Google Cloud Console](https://console.cloud.google.com/)
   - 創建新項目或選擇現有項目
   - 啟用 Vertex AI API 和 Generative AI API

2. **創建服務帳戶:**
   - 導航到 IAM 和管理 > 服務帳戶
   - 點擊"創建服務帳戶"
   - 分配角色："Vertex AI 用戶"和"AI Platform 開發者"
   - 生成並下載 JSON 密鑰文件

3. **配置憑證:**
   - 將 JSON 密鑰文件放在項目根目錄
   - 如果文件名與默認不同，請更新 `utils_gemini.py` 中的文件名
   - 設置環境變量（可選）:
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/keyfile.json"
     ```

### 步驟 4: 應用程序配置

1. **編輯配置文件:**
   ```bash
   cp config.yaml config.yaml.backup  # 備份原文件
   nano config.yaml  # 使用您喜歡的編輯器編輯
   ```

2. **主要配置選項:**
   ```yaml
   ocr_lang: eng  # OCR 語言: 'eng', 'chi_tra', 'eng+chi_tra'
   
   # 如需要可添加自定義分析器
   analyzers:
     Custom_Analyzer:
       enabled: true
   ```

3. **創建上傳目錄:**
   ```bash
   mkdir -p uploads logs
   chmod 755 uploads logs
   ```

### 步驟 5: 數據庫初始化

應用程序將在首次運行時自動創建 SQLite 數據庫。默認管理員憑證：
- **用戶名**: `admin`
- **密碼**: `admin123`

**重要**: 首次登錄後請更改默認管理員密碼！

### 步驟 6: 啟動應用程序

1. **運行應用程序:**
   ```bash
   python app.py
   ```

2. **訪問網頁界面:**
   - 打開瀏覽器
   - 導航到 `http://localhost:5000`
   - 使用管理員憑證登錄

### 步驟 7: 驗證

1. **測試文件上傳:**
   - 上傳示例 PDF 或圖像文件
   - 選擇分析類型
   - 驗證處理成功完成

2. **檢查日誌:**
   ```bash
   tail -f logs/test_log.txt
   ```

### 故障排除

#### 常見問題

**1. 找不到 Tesseract:**
```bash
# 驗證 Tesseract 安裝
tesseract --version

# 如果找不到，檢查 PATH 或重新安裝
```

**2. Google API 身份驗證錯誤:**
- 驗證 JSON 密鑰文件路徑和權限
- 檢查 Google Cloud Console 中是否啟用了 API
- 確保服務帳戶具有適當的角色

**3. PDF 處理錯誤:**
```bash
# 驗證 Poppler 安裝
pdftoppm -h

# 如果找不到，重新安裝 Poppler
```

**4. 大文件內存問題:**
- 增加系統內存
- 以較小批次處理文件
- 調整 app.py 中的 `MAX_CONTENT_LENGTH`

**5. 端口已被使用:**
```bash
# 查找使用端口 5000 的進程
lsof -i :5000

# 終止進程或使用不同端口
python app.py --port 5001
```

### 生產部署

對於生產部署，請考慮：

1. **使用生產 WSGI 服務器:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **設置反向代理 (Nginx):**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

3. **配置 SSL 證書**
4. **設置監控和日誌記錄**
5. **配置備份程序**