# BakuDocs Smart Document Analysis System

[中文版本](#中文版本) | [English Version](#english-version)

---

## English Version

### Overview

BakuDocs is an intelligent document analysis system powered by AI that can automatically extract, analyze, and process various types of documents. The system uses Google Gemini AI to provide accurate document analysis with support for multiple document formats and analysis types.

### Key Features

- **Multi-format Document Support**: PDF, Word (DOC/DOCX), Excel (XLS/XLSX), CSV, TXT, and image files (JPG, PNG, BMP)
- **AI-Powered Analysis**: Leverages Google Gemini 2.5 Pro for intelligent document processing
- **Multiple Analysis Types**:
  - **Cargo Bill of Lading (BL)**: Maritime shipping document analysis
  - **Invoice Processing**: Commercial invoice data extraction
  - **Table Analysis**: Structured data extraction from tables
  - **Calendar Analysis**: Date and schedule information extraction
- **OCR Support**: Automatic text extraction from images and scanned documents
- **User Management**: Multi-user system with admin controls and permissions
- **Export Capabilities**: Generate formatted Excel reports with logos and custom styling
- **Batch Processing**: Handle multiple files simultaneously
- **Progress Tracking**: Real-time processing status updates
- **History Management**: Track all analysis activities with detailed logs

### Technology Stack

- **Backend**: Flask (Python web framework)
- **AI Engine**: Google Gemini 2.5 Pro API
- **Database**: SQLite for user management and settings
- **Document Processing**: 
  - PDFPlumber for PDF text extraction
  - python-docx for Word documents
  - pandas/openpyxl for Excel files
  - pytesseract for OCR
- **Frontend**: HTML5, CSS3, JavaScript with modern UI design
- **Authentication**: Session-based user authentication with password hashing

### 🚀 Quick Start with Docker/Podman (Recommended)

The easiest way to deploy BakuDocs is using containers:

#### Docker (Traditional)
```bash
# Clone the repository
git clone <repository-url>
cd bakudocs-document-analyzer

# One-click setup
./setup_docker.sh

# Or manual setup
docker-compose up -d
```

#### Podman (Modern Alternative)
```bash
# Clone the repository
git clone <repository-url>
cd bakudocs-document-analyzer

# One-click setup with Podman
./setup_podman.sh

# Or manual setup
docker-compose -f docker-compose.podman.yml up -d
```

Access the application at: http://localhost:5001

📚 **For detailed deployment instructions, see:**
- **Docker**: [`DOCKER_DEPLOYMENT.md`](DOCKER_DEPLOYMENT.md)
- **Podman**: [`PODMAN_DEPLOYMENT.md`](PODMAN_DEPLOYMENT.md)

### Installation (Manual Setup)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd bakudocs-document-analyzer
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Cloud credentials**:
   - Place your Google Cloud service account JSON file in the project root
   - Update the filename in `utils_gemini.py` if different from `fileanalyzer-463911-e71c7f7288ad.json`

5. **Install Tesseract OCR**:
   - **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
   - **macOS**: `brew install tesseract`
   - **Windows**: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)

### Configuration

1. **Edit `config.yaml`**:
   - Configure OCR language settings
   - Adjust analysis parameters
   - Set up custom prompts if needed

2. **Database initialization**:
   - The system automatically creates SQLite database on first run
   - Default admin account: username `admin`, password `admin123`

### Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Access the web interface**:
   - Open browser and navigate to `http://localhost:5000`
   - Login with admin credentials or create user accounts

3. **Document Analysis**:
   - Upload single or multiple documents
   - Select analysis type (Cargo BL, Invoice, Table Analysis, Calendar)
   - Configure analysis options (OCR language, VLM settings)
   - Monitor progress and download results

4. **Admin Features**:
   - User management and permissions
   - Analyzer configuration per user
   - System usage statistics
   - History management

### API Integration

The system supports both cloud and local AI models:
- **Cloud**: Google Gemini 2.5 Pro (default)
- **Local**: Ollama integration for on-premises deployment

### File Structure

```
bakudocs-document-analyzer/
├── app.py                 # Main Flask application
├── config.yaml           # Configuration settings
├── requirements.txt       # Python dependencies
├── utils_gemini.py       # Google Gemini API integration
├── analyzers/            # Analysis modules
│   ├── clients/          # AI client implementations
│   ├── common/           # Shared utilities
│   └── services/         # Analysis services and prompts
├── templates/            # HTML templates
├── static/              # CSS, JS, images
├── uploads/             # File upload directory
└── logs/                # Application logs
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### License

This project is licensed under the MIT License - see the LICENSE file for details.

### Support

For support and questions, please create an issue in the repository or contact the development team.

---

## 中文版本

### 概述

BakuDocs 是一個基於人工智能的智能文檔分析系統，能夠自動提取、分析和處理各種類型的文檔。系統使用 Google Gemini AI 提供準確的文檔分析，支持多種文檔格式和分析類型。

### 主要功能

- **多格式文檔支持**: PDF、Word (DOC/DOCX)、Excel (XLS/XLSX)、CSV、TXT 和圖像文件 (JPG, PNG, BMP)
- **AI 驅動分析**: 利用 Google Gemini 2.5 Pro 進行智能文檔處理
- **多種分析類型**:
  - **貨運提單 (BL)**: 海運文檔分析
  - **發票處理**: 商業發票數據提取
  - **表格分析**: 從表格中提取結構化數據
  - **日曆分析**: 日期和時間表信息提取
- **OCR 支持**: 自動從圖像和掃描文檔中提取文字
- **用戶管理**: 多用戶系統，具有管理員控制和權限管理
- **導出功能**: 生成帶有標誌和自定義樣式的格式化 Excel 報告
- **批量處理**: 同時處理多個文件
- **進度跟踪**: 實時處理狀態更新
- **歷史管理**: 跟踪所有分析活動並提供詳細日誌

### 技術棧

- **後端**: Flask (Python 網頁框架)
- **AI 引擎**: Google Gemini 2.5 Pro API
- **數據庫**: SQLite 用於用戶管理和設置
- **文檔處理**: 
  - PDFPlumber 用於 PDF 文字提取
  - python-docx 用於 Word 文檔
  - pandas/openpyxl 用於 Excel 文件
  - pytesseract 用於 OCR
- **前端**: HTML5、CSS3、JavaScript 現代化 UI 設計
- **身份驗證**: 基於會話的用戶身份驗證，使用密碼哈希

### 🚀 Docker/Podman 快速開始（推薦）

使用容器部署 BakuDocs 是最簡單的方式：

#### Docker（傳統方式）
```bash
# 克隆倉庫
git clone <repository-url>
cd bakudocs-document-analyzer

# 一鍵設置
./setup_docker.sh

# 或手動設置
docker-compose up -d
```

#### Podman（現代替代方案）
```bash
# 克隆倉庫
git clone <repository-url>
cd bakudocs-document-analyzer

# 使用 Podman 一鍵設置
./setup_podman.sh

# 或手動設置
docker-compose -f docker-compose.podman.yml up -d
```

訪問應用程式：http://localhost:5001

📚 **詳細的部署說明請參閱：**
- **Docker**: [`DOCKER_DEPLOYMENT.md`](DOCKER_DEPLOYMENT.md)
- **Podman**: [`PODMAN_DEPLOYMENT.md`](PODMAN_DEPLOYMENT.md)

### 安裝（手動設置）

1. **克隆倉庫**:
   ```bash
   git clone <repository-url>
   cd bakudocs-document-analyzer
   ```

2. **創建虛擬環境**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **安裝依賴**:
   ```bash
   pip install -r requirements.txt
   ```

4. **設置 Google Cloud 憑證**:
   - 將 Google Cloud 服務帳戶 JSON 文件放在項目根目錄
   - 如果文件名不同於 `fileanalyzer-463911-e71c7f7288ad.json`，請更新 `utils_gemini.py` 中的文件名

5. **安裝 Tesseract OCR**:
   - **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
   - **macOS**: `brew install tesseract`
   - **Windows**: 從 [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki) 下載

### 配置

1. **編輯 `config.yaml`**:
   - 配置 OCR 語言設置
   - 調整分析參數
   - 如需要可設置自定義提示詞

2. **數據庫初始化**:
   - 系統在首次運行時自動創建 SQLite 數據庫
   - 默認管理員帳戶: 用戶名 `admin`，密碼 `admin123`

### 使用方法

1. **啟動應用程序**:
   ```bash
   python app.py
   ```

2. **訪問網頁界面**:
   - 打開瀏覽器並導航到 `http://localhost:5000`
   - 使用管理員憑證登錄或創建用戶帳戶

3. **文檔分析**:
   - 上傳單個或多個文檔
   - 選擇分析類型（貨運提單、發票、表格分析、日曆）
   - 配置分析選項（OCR 語言、VLM 設置）
   - 監控進度並下載結果

4. **管理員功能**:
   - 用戶管理和權限設置
   - 每個用戶的分析器配置
   - 系統使用統計
   - 歷史記錄管理

### API 集成

系統支持雲端和本地 AI 模型:
- **雲端**: Google Gemini 2.5 Pro (默認)
- **本地**: Ollama 集成，支持本地部署

### 文件結構

```
bakudocs-document-analyzer/
├── app.py                 # 主 Flask 應用程序
├── config.yaml           # 配置設置
├── requirements.txt       # Python 依賴
├── utils_gemini.py       # Google Gemini API 集成
├── analyzers/            # 分析模塊
│   ├── clients/          # AI 客戶端實現
│   ├── common/           # 共享工具
│   └── services/         # 分析服務和提示詞
├── templates/            # HTML 模板
├── static/              # CSS、JS、圖像
├── uploads/             # 文件上傳目錄
└── logs/                # 應用程序日誌
```

### 貢獻

1. Fork 倉庫
2. 創建功能分支
3. 進行更改
4. 如適用，添加測試
5. 提交拉取請求

### 許可證

本項目採用 MIT 許可證 - 詳情請參閱 LICENSE 文件。

### 支持

如需支持和問題諮詢，請在倉庫中創建 issue 或聯繫開發團隊。