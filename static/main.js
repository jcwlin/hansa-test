const langsDict = JSON.parse(document.getElementById('langs-data').textContent);
function getCurrentLang() {
    // 先抓 select[name="lang"]，抓不到再抓 input
    return document.querySelector('select[name="lang"]')?.value ||
           document.querySelector('input[name="lang"]')?.value || 'zh';
}
function getLangText(key) {
    const lang = getCurrentLang();
    return (langsDict[lang] && langsDict[lang][key]) || key;
}

// 用來存儲所有選中的檔案 - 全域變數
let selectedFiles = [];

// DOM 載入完成後執行
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded');
    
    // 獲取所有需要的元素
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('files');
    const selectFilesBtn = document.getElementById('select-files-btn');
    
    console.log('Elements found:', {
        dropzone: !!dropzone,
        fileInput: !!fileInput,
        selectFilesBtn: !!selectFilesBtn
    });
    const analyzeForm = document.getElementById('analyze-form');
    const startBtn = document.getElementById('start-analysis');
    const clearBtn = document.getElementById('clear-files');
    const analysisType = document.getElementById('analysis_type');
    const promptBox = document.getElementById('prompt');
    const previewTitleInput = document.getElementById('preview-title-input');
    const previewTitle = document.getElementById('preview-title');
    const editPreviewTitleBtn = document.getElementById('edit-preview-title');

    // 檔案選擇按鈕點擊事件
    if (selectFilesBtn && fileInput) {
        selectFilesBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            console.log('Select files button clicked');
            fileInput.click();
        });
    }

    // 拖曳上傳功能
    if (dropzone && fileInput) {
        dropzone.addEventListener('dragover', function(e) {
            e.preventDefault();
            dropzone.classList.add('dragover');
        });

        dropzone.addEventListener('dragleave', function(e) {
            e.preventDefault();
            dropzone.classList.remove('dragover');
        });

        dropzone.addEventListener('drop', function(e) {
            e.preventDefault();
            dropzone.classList.remove('dragover');
            if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
                // 累加新檔案到現有檔案列表
                addFilesToSelection(Array.from(e.dataTransfer.files));
            }
        });

        // 點擊拖曳區域也能選擇檔案（但不包含按鈕）
        dropzone.addEventListener('click', function(e) {
            // 如果點擊的是按鈕，不觸發檔案選擇
            if (e.target.id === 'select-files-btn' || e.target.closest('#select-files-btn')) {
                return;
            }
            console.log('Dropzone clicked');
            fileInput.click();
        });
    }

    // 檔案選擇變更事件
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            console.log('Files selected:', this.files.length);
            // 累加新檔案到現有檔案列表
            if (this.files.length > 0) {
                addFilesToSelection(Array.from(this.files));
                // 清空 input 以便下次選擇相同檔案
                this.value = '';
            }
        });
    }

    // 添加檔案到選擇列表
    function addFilesToSelection(newFiles) {
        for (let file of newFiles) {
            // 檢查是否已經存在同名檔案
            const existingIndex = selectedFiles.findIndex(f => f.name === file.name && f.size === file.size);
            if (existingIndex === -1) {
                selectedFiles.push(file);
            }
        }
        updateFileInput();
        updateStats();
        updateFileList();
    }

    // 從選擇列表移除檔案
    function removeFileFromSelection(index) {
        selectedFiles.splice(index, 1);
        updateFileInput();
        updateStats();
        updateFileList();
    }

    // 更新 file input 的 files 屬性
    function updateFileInput() {
        const dt = new DataTransfer();
        for (let file of selectedFiles) {
            dt.items.add(file);
        }
        if (fileInput) {
            fileInput.files = dt.files;
        }
    }

    // 更新統計資訊
    function updateStats() {
        const statFiles = document.getElementById('stat-files');
        const statSize = document.getElementById('stat-size');
        
        if (statFiles) {
            statFiles.innerText = selectedFiles.length;
        }
        
        if (statSize) {
            let size = 0;
            for (let file of selectedFiles) {
                size += file.size;
            }
            if (size < 1024) {
                statSize.innerText = size.toFixed(1) + ' B';
            } else if (size < 1024 * 1024) {
                statSize.innerText = (size / 1024).toFixed(1) + ' KB';
            } else {
                statSize.innerText = (size / (1024 * 1024)).toFixed(1) + ' MB';
            }
        }
    }

    // 更新檔案列表顯示
    function updateFileList() {
        const fileList = document.getElementById('file-list');
        if (!fileList) return;

        if (selectedFiles.length === 0) {
            const currentLang = document.querySelector('input[name="lang"]')?.value || 'en';
            let noFilesText;
            if (currentLang === 'zh') {
                noFilesText = '尚未選擇檔案';
            } else if (currentLang === 'nor') {
                noFilesText = 'Ingen filer valgt';
            } else {
                noFilesText = 'No files selected';
            }
            fileList.innerHTML = `<div style="color: #999; font-style: italic;">${noFilesText}</div>`;
            return;
        }

        const currentLang = document.querySelector('input[name="lang"]')?.value || 'en';
        let removeTooltip;
        if (currentLang === 'zh') {
            removeTooltip = '移除檔案';
        } else if (currentLang === 'nor') {
            removeTooltip = 'Fjern fil';
        } else {
            removeTooltip = 'Remove file';
        }

        let html = '';
        selectedFiles.forEach((file, index) => {
            let sizeText;
            if (file.size < 1024) {
                sizeText = file.size + ' B';
            } else if (file.size < 1024 * 1024) {
                sizeText = (file.size / 1024).toFixed(1) + ' KB';
            } else {
                sizeText = (file.size / (1024 * 1024)).toFixed(1) + ' MB';
            }

            html += `
                <div class="file-item">
                    <div class="file-info">
                        <div class="file-name" title="${file.name}">${file.name}</div>
                        <div class="file-size">${sizeText}</div>
                    </div>
                    <button class="file-remove" onclick="removeFileFromSelection(${index})" title="${removeTooltip}">×</button>
                </div>
            `;
        });
        fileList.innerHTML = html;
    }

    // 將 removeFileFromSelection 函數設為全域，讓 HTML 能夠調用
    window.removeFileFromSelection = removeFileFromSelection;

    // 開始分析按鈕
    if (startBtn && analyzeForm) {
        startBtn.addEventListener('click', function() {
            console.log('分析按鈕被點擊，檔案數量：', selectedFiles.length);
            analyzeForm.dispatchEvent(new Event('submit'));
        });
    } else {
        console.log('按鈕或表單元素未找到：', {
            startBtn: !!startBtn,
            analyzeForm: !!analyzeForm
        });
    }

    // 清除檔案按鈕
    if (clearBtn && fileInput) {
        clearBtn.addEventListener('click', function() {
            selectedFiles = [];
            fileInput.value = '';
            updateStats();
            updateFileList();
            const resultArea = document.getElementById('result-area');
            if (resultArea) {
                resultArea.style.display = 'none';
            }
        });
    }

    // 初始化顯示
    updateStats();
    updateFileList();

    // 不再自動填入 prompt，讓 Advanced Options 保持空白
    // 用戶可以手動輸入自訂的 prompt

    if (previewTitleInput) {
        previewTitleInput.addEventListener('input', function() {
            // 你可以根據需求同步到其他區塊
            // 例如同步到 h5.card-title（如果還有）
            const cardTitle = document.querySelector('.card-title');
            if (cardTitle) {
                cardTitle.textContent = this.value;
            }
        });
    }

    if (editPreviewTitleBtn && previewTitle) {
        editPreviewTitleBtn.addEventListener('click', function() {
            // 建立 input
            const input = document.createElement('input');
            input.type = 'text';
            input.className = 'form-control form-control-sm';
            input.value = previewTitle.textContent;
            input.style.fontWeight = 'bold';
            input.style.fontSize = '1.1em';
            input.style.maxWidth = '350px';
            previewTitle.replaceWith(input);
            input.focus();
            // 完成編輯時還原
            function finishEdit() {
                previewTitle.textContent = input.value;
                input.replaceWith(previewTitle);
            }
            input.addEventListener('blur', finishEdit);
            input.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') {
                    input.blur();
                }
            });
        });
    }
});

// 表單提交處理
document.getElementById('analyze-form').onsubmit = function(e) {
    e.preventDefault();
    
    // 檢查是否有選擇檔案
    if (selectedFiles.length === 0) {
        showError('錯誤', '請先選擇檔案');
        return false;
    }
    
    // 手動建立 FormData，加入所有選中的檔案
    let form = new FormData();
    
    // 添加所有選中的檔案
    for (let file of selectedFiles) {
        form.append('file', file);
    }
    
    // 添加其他表單欄位
    form.append('lang', document.querySelector('input[name="lang"]').value);
    form.append('analysis_type', document.getElementById('analysis_type').value);
    form.append('custom_prompt', document.getElementById('prompt').value);
    // 新增 keep_filename 狀態
    form.append('keep_filename', document.getElementById('keep_filename').checked ? '1' : '0');
    
    console.log('提交檔案數量：', selectedFiles.length);
    for (let file of selectedFiles) {
        console.log('檔案：', file.name, '大小：', file.size);
    }
    
    let progressArea = document.getElementById('progress-area');
    let progressBar = document.getElementById('progress-bar');
    let analyzingLabel = document.getElementById('analyzing-label');
    let resultArea = document.getElementById('result-area');
    let resultTable = document.getElementById('result-table');
    let exportBtn = document.getElementById('export-btn');
    let langDetect = document.getElementById('lang-detect');
    
    // 顯示進度條
    progressArea.style.display = '';
    progressBar.style.width = '0%';
    analyzingLabel.innerText = getLangText('analyzing');
    resultArea.style.display = 'none';
    
    // 提交表單
    fetch('/analyze', {method:'POST', body:form})
        .then(r => r.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            
            // 開始進度追蹤
            const taskId = data.task_id;
            startProgressTracking(taskId, data);
        })
        .catch(err => {
            progressArea.style.display = 'none';
            showError('分析失敗', err);
        });
    
    return false;
};

function startProgressTracking(taskId, finalData) {
    const progressBar = document.getElementById('progress-bar');
    const analyzingLabel = document.getElementById('analyzing-label');
    const resultArea = document.getElementById('result-area');
    const resultTable = document.getElementById('result-table');
    const exportBtn = document.getElementById('export-btn');
    const langDetect = document.getElementById('lang-detect');
    const progressArea = document.getElementById('progress-area');
    
    // 取得當前語言
    const currentLang = getCurrentLang();
    
    // 開始計時
    const startTime = Date.now();
    
    // 定期查詢進度
    const progressInterval = setInterval(() => {
        fetch(`/progress/${taskId}`)
            .then(r => {
                if (!r.ok) {
                    throw new Error(`HTTP ${r.status}: ${r.statusText}`);
                }
                return r.json();
            })
            .then(response => {
                // 首先檢查回應是否有效
                if (!response) {
                    throw new Error('Empty response from server');
                }
                
                console.log('Progress response:', response); // Debug log
                
                // 檢查是否為最終結果
                if (response.success !== undefined) {
                    clearInterval(progressInterval);
                    // 重置錯誤計時器
                    window.progressErrorStartTime = null;
                    
                    if (response.success) {
                        // 計算最終時間
                        const elapsedTime = Math.floor((Date.now() - startTime) / 1000);
                        const minutes = Math.floor(elapsedTime / 60);
                        const seconds = elapsedTime % 60;
                        const timeStr = minutes > 0 ? `${minutes}:${seconds.toString().padStart(2, '0')}` : `${seconds}s`;
                        
                        // 顯示完成狀態
                        let completedMessage = '';
                        if (currentLang === 'zh') {
                            completedMessage = `${getLangText('analysis_complete')}! ${getLangText('time')}: ${timeStr}`;
                        } else if (currentLang === 'nor') {
                            completedMessage = `${getLangText('analysis_complete')}! ${getLangText('time')}: ${timeStr}`;
                        } else {
                            completedMessage = `${getLangText('analysis_complete')}! ${getLangText('time')}: ${timeStr}`;
                        }
                        
                        progressBar.style.width = '100%';
                        analyzingLabel.innerText = completedMessage;
                        
                        // 顯示 Total Page/Cost Time
                        const statTotalPageValue = document.getElementById('stat-total-page-value');
                        const statTotalPageTime = document.getElementById('stat-total-page-time');
                        if (statTotalPageValue && statTotalPageTime) {
                            statTotalPageValue.innerText = `0 / ${timeStr}`;
                            statTotalPageTime.style.display = '';
                        }
                        
                        const statCostTime = document.getElementById('stat-cost-time');
                        const statCostTimeValue = document.getElementById('stat-cost-time-value');
                        if (statCostTime && statCostTimeValue) {
                            statCostTimeValue.innerText = timeStr;
                            statCostTime.style.display = '';
                        }
                        
                        // 延遲顯示結果
                        setTimeout(() => {
                            progressArea.style.display = 'none';
                            resultArea.style.display = '';
                            
                            // 顯示語言
                            langDetect.innerText = 'Detected language: ' + (response.lang_code || 'unknown');
                            
                            // 顯示表格
                            renderTable(response.headers, response.rows);
                            
                            // 設定匯出按鈕
                            exportBtn.onclick = function() {
                                // 取得目前 headers
                                const table = document.getElementById('result-table');
                                const thead = table.querySelector('thead');
                                const headers = [];
                                if (thead) {
                                    thead.querySelectorAll('th').forEach(th => headers.push(th.textContent));
                                }
                                // 取得目前 rows
                                const rows = [];
                                const tbody = table.querySelector('tbody');
                                if (tbody) {
                                    tbody.querySelectorAll('tr').forEach(tr => {
                                        const row = [];
                                        tr.querySelectorAll('td').forEach(td => row.push(td.textContent));
                                        rows.push(row);
                                    });
                                }
                                
                                // 取得手動插入的資料
                                const manualData = getManualInsertionData();
                                
                                // 取得 logo 選項
                                const includeLogo = document.getElementById('include_logo')?.checked || false;
                                
                                // 取得預覽標題
                                const previewTitle = document.getElementById('preview-title')?.textContent || 'Hansa Tankers';
                                
                                // 傳送到後端
                                fetch('/export_custom', {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify({ 
                                        headers, 
                                        rows,
                                        manual_data: manualData,
                                        include_logo: includeLogo,
                                        preview_title: previewTitle
                                    })
                                })
                                .then(r => r.json())
                                .then(data => {
                                    if (data.success && data.download_url) {
                                        window.location = data.download_url;
                                    } else {
                                        showError('匯出失敗', data.error || '未知錯誤');
                                    }
                                })
                                .catch(err => {
                                    showError('匯出失敗', err);
                                });
                            };
                        }, 1500);
                    } else {
                        // 處理錯誤 - 停止進度追蹤
                        clearInterval(progressInterval);
                        // 重置錯誤計時器
                        window.progressErrorStartTime = null;
                        
                        const currentLang = getCurrentLang();
                        let errorMessage = '';
                        if (currentLang === 'zh') {
                            errorMessage = '分析失敗: ' + (response.error || '未知錯誤');
                        } else {
                            errorMessage = 'Analysis failed: ' + (response.error || 'Unknown error');
                        }
                        
                        analyzingLabel.innerText = errorMessage;
                        progressBar.style.width = '100%';
                        progressBar.classList.add('bg-danger');
                        
                        // 顯示錯誤對話框
                        alert(errorMessage);
                        // 重置UI（可選）
                        setTimeout(() => {
                            location.reload();
                        }, 3000);
                    }
                    return;
                }
                
                // 正常進度更新
                const progress = response;
                
                // 驗證進度數據是否有效 - 更寬鬆的檢查
                if (!progress || (typeof progress !== 'object')) {
                    throw new Error('Invalid progress data received');
                }
                
                // 如果回應中有 success 字段但不是 undefined，說明是最終結果，不需要檢查進度字段
                if (progress.success !== undefined) {
                    // 這是最終結果，直接處理
                    if (progress.success) {
                        // 分析成功，顯示結果
                        clearInterval(progressInterval);
                        window.progressErrorStartTime = null;
                        
                        // 延遲顯示結果，讓進度條到100%
                        setTimeout(() => {
                            progressArea.style.display = 'none';
                            resultArea.style.display = '';
                            
                            // 顯示數據表格
                            const headers = progress.headers || [];
                            const rows = progress.rows || [];
                            
                            // 建構表格
                            let tableHTML = '<table class="table table-striped table-bordered table-hover"><thead class="table-dark">';
                            
                            if (headers.length > 0) {
                                tableHTML += '<tr>';
                                headers.forEach(header => {
                                    tableHTML += `<th>${header}</th>`;
                                });
                                tableHTML += '</tr></thead><tbody>';
                                
                                // 添加數據行
                                rows.forEach(row => {
                                    tableHTML += '<tr>';
                                    if (Array.isArray(row)) {
                                        row.forEach(cell => {
                                            tableHTML += `<td>${cell || ''}</td>`;
                                        });
                                    } else {
                                        // 如果是物件，按照headers順序提取值
                                        headers.forEach(header => {
                                            tableHTML += `<td>${row[header] || ''}</td>`;
                                        });
                                    }
                                    tableHTML += '</tr>';
                                });
                                
                                tableHTML += '</tbody></table>';
                                resultTable.innerHTML = tableHTML;
                            }
                            
                            // 設置下載按鈕
                            if (progress.excel) {
                                exportBtn.onclick = () => {
                                    window.location = `/export/${progress.excel}`;
                                };
                                exportBtn.style.display = '';
                            }
                        }, 500);
                        return;
                    } else {
                        // 分析失敗，但這裡應該已經在前面處理了
                        clearInterval(progressInterval);
                        window.progressErrorStartTime = null;
                        
                        const currentLang = getCurrentLang();
                        let errorMessage = '';
                        if (currentLang === 'zh') {
                            errorMessage = '分析失敗: ' + (progress.error || '未知錯誤');
                        } else {
                            errorMessage = 'Analysis failed: ' + (progress.error || 'Unknown error');
                        }
                        
                        analyzingLabel.innerText = errorMessage;
                        progressBar.style.width = '100%';
                        progressBar.classList.add('bg-danger');
                        
                        alert(errorMessage);
                        setTimeout(() => {
                            location.reload();
                        }, 3000);
                        return;
                    }
                }
                
                // 如果不是最終結果，檢查進度字段
                if (progress.percentage === undefined && progress.current === undefined && progress.message === undefined) {
                    throw new Error('Invalid progress data received - no progress indicators');
                }
                
                // 重置錯誤計時器，因為我們成功獲取了進度
                window.progressErrorStartTime = null;
                
                // 計算經過時間
                const elapsedTime = Math.floor((Date.now() - startTime) / 1000);
                const minutes = Math.floor(elapsedTime / 60);
                const seconds = elapsedTime % 60;
                const timeStr = minutes > 0 ? `${minutes}:${seconds.toString().padStart(2, '0')}` : `${seconds}s`;
                
                // 進度中
                let statusMessage = '';
                
                // 確保有文件計數信息
                const currentFiles = progress.current || 0;
                const totalFiles = progress.total || 1;
                const percentage = Math.round(progress.percentage || 0);
                
                if (currentLang === 'zh') {
                    statusMessage = `分析中 ${currentFiles}/${totalFiles} 檔案 (${percentage}%) | 時間: ${timeStr}`;
                } else if (currentLang === 'nor') {
                    statusMessage = `Analyserer ${currentFiles}/${totalFiles} filer (${percentage}%) | Tid: ${timeStr}`;
                } else {
                    statusMessage = `Analyzing ${currentFiles}/${totalFiles} files (${percentage}%) | Time: ${timeStr}`;
                }
                
                // 如果有自訂訊息，結合文件計數顯示
                if (progress.message && !progress.message.includes('已完成') && !progress.message.includes('檔案')) {
                    if (currentLang === 'zh') {
                        statusMessage = `${progress.message} ${currentFiles}/${totalFiles} (${percentage}%) | 時間: ${timeStr}`;
                    } else if (currentLang === 'nor') {
                        statusMessage = `${progress.message} ${currentFiles}/${totalFiles} (${percentage}%) | Tid: ${timeStr}`;
                    } else {
                        statusMessage = `${progress.message} ${currentFiles}/${totalFiles} (${percentage}%) | Time: ${timeStr}`;
                    }
                }
                
                // 更新進度條
                progressBar.style.width = progress.percentage + '%';
                analyzingLabel.innerText = statusMessage;
            })
            .catch(err => {
                console.error('Progress tracking error:', err);
                // 當網絡錯誤時，顯示更友好的錯誤信息而非直接清除間隔
                const currentLang = getCurrentLang();
                let errorMessage = '';
                if (currentLang === 'zh') {
                    errorMessage = `連接錯誤，重試中... (${err.message || err})`;
                } else {
                    errorMessage = `Connection error, retrying... (${err.message || err})`;
                }
                
                // 更新顯示但不清除間隔，讓它繼續重試
                const analyzingLabel = document.getElementById('analyzing-label');
                if (analyzingLabel) {
                    analyzingLabel.innerText = errorMessage;
                }
                
                // 如果錯誤持續太久（比如超過 30 秒），才停止
                const currentTime = Date.now();
                if (!window.progressErrorStartTime) {
                    window.progressErrorStartTime = currentTime;
                } else if (currentTime - window.progressErrorStartTime > 30000) {
                    clearInterval(progressInterval);
                    if (currentLang === 'zh') {
                        showError('進度追蹤失敗', '無法獲取分析進度，請重新開始分析。');
                    } else {
                        showError('Progress Tracking Failed', 'Cannot get analysis progress, please restart analysis.');
                    }
                }
            });
    }, 1000); // 每秒查詢一次進度
}

function showError(title, msg) {
    let modal = new bootstrap.Modal(document.getElementById('error-modal'));
    document.getElementById('error-message').innerText = msg;
    modal.show();
}

function copyError() {
    let msg = document.getElementById('error-message').innerText;
    navigator.clipboard.writeText(msg);
}

function renderTable(headers, rows) {
    const table = document.getElementById('result-table');
    table.innerHTML = '';
    
    // 表格標題
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    headerRow.className = 'table-dark';
    
    headers.forEach((header, i) => {
        const th = document.createElement('th');
        th.textContent = header;
        th.style.whiteSpace = 'nowrap';
        th.style.cursor = 'pointer';
        th.title = 'Click to edit';
        th.addEventListener('click', function() {
            const input = document.createElement('input');
            input.type = 'text';
            input.value = th.textContent;
            input.className = 'form-control form-control-sm';
            input.style.minWidth = '80px';
            th.textContent = '';
            th.appendChild(input);
            input.focus();
            input.addEventListener('blur', finishEdit);
            input.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') input.blur();
            });
            function finishEdit() {
                headers[i] = input.value;
                th.textContent = input.value;
            }
        });
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    // 表格內容
    const tbody = document.createElement('tbody');
    
    rows.forEach((rowObj, index) => {
        const tr = document.createElement('tr');
        
        // 檢查是否為總計行或貨物數量行
        if (rowObj.is_total) {
            tr.className = 'table-warning fw-bold';  // 黃色背景，粗體
        } else if (rowObj.is_cgos) {
            tr.className = 'table-info fw-bold';     // 藍色背景，粗體
        }
        
        // 使用 rowObj.data 來獲取實際資料
        const rowData = rowObj.data || rowObj;
        
        headers.forEach((header, headerIndex) => {
            const td = document.createElement('td');
            // 如果 rowData 是陣列，使用索引；如果是物件，使用 header 名稱
            const value = Array.isArray(rowData) ? rowData[headerIndex] : rowData[header];
            td.textContent = value !== null && value !== undefined ? value : '';
            td.style.whiteSpace = 'nowrap';
            tr.appendChild(td);
        });
        
        tbody.appendChild(tr);
    });
    
    table.appendChild(tbody);
}

// Manual Insertion 功能
document.addEventListener('DOMContentLoaded', function() {
    // 確保所有 Manual Insertion 相關的元素都已載入
    const addRowBtn = document.getElementById('add-row-btn');
    const removeRowBtn = document.getElementById('remove-row-btn');
    const addColumnBtn = document.getElementById('add-column-btn');
    const removeColumnBtn = document.getElementById('remove-column-btn');
    const manualTable = document.getElementById('manual-table');
    
    if (addRowBtn && removeRowBtn && addColumnBtn && removeColumnBtn && manualTable) {
        // 添加列
        addRowBtn.addEventListener('click', function() {
            const tbody = manualTable.querySelector('tbody');
            const thead = manualTable.querySelector('thead');
            const columnCount = thead.querySelectorAll('th').length;
            
            // 如果沒有欄位，先創建一個欄位
            if (columnCount === 0) {
                addColumnBtn.click();
                return;
            }
            
            const newRow = document.createElement('tr');
            for (let i = 0; i < columnCount; i++) {
                const td = document.createElement('td');
                const input = document.createElement('input');
                input.type = 'text';
                input.className = 'form-control form-control-sm manual-input';
                input.placeholder = getLangText('value');
                // 新增顏色選擇器
                const colorInput = document.createElement('input');
                colorInput.type = 'color';
                colorInput.className = 'manual-color-input ms-1';
                colorInput.value = '#000000';
                // 新增字體大小 input
                const fontSizeInput = document.createElement('input');
                fontSizeInput.type = 'number';
                fontSizeInput.className = 'manual-fontsize-input ms-1';
                fontSizeInput.value = 12;
                fontSizeInput.min = 8;
                fontSizeInput.max = 48;
                fontSizeInput.style.width = '48px';
                fontSizeInput.title = '字體大小';
                td.appendChild(input);
                td.appendChild(colorInput);
                td.appendChild(fontSizeInput);
                newRow.appendChild(td);
            }
            tbody.appendChild(newRow);
        });
        
        // 移除列
        removeRowBtn.addEventListener('click', function() {
            const tbody = manualTable.querySelector('tbody');
            const rows = tbody.querySelectorAll('tr');
            if (rows.length > 0) {
                tbody.removeChild(rows[rows.length - 1]);
            }
        });
        
        // 添加欄
        addColumnBtn.addEventListener('click', function() {
            const thead = manualTable.querySelector('thead');
            const tbody = manualTable.querySelector('tbody');
            const currentColumnCount = thead.querySelectorAll('th').length;
            
            // 添加表頭
            const headerRow = thead.querySelector('tr');
            const newTh = document.createElement('th');
            newTh.style.minWidth = '100px';
            newTh.textContent = getLangText('column') + ' ' + (currentColumnCount + 1);
            headerRow.appendChild(newTh);
            
            // 為每一列添加新的輸入框
            const rows = tbody.querySelectorAll('tr');
            rows.forEach(row => {
                const td = document.createElement('td');
                const input = document.createElement('input');
                input.type = 'text';
                input.className = 'form-control form-control-sm manual-input';
                input.placeholder = getLangText('value');
                
                // 新增顏色選擇器
                const colorInput = document.createElement('input');
                colorInput.type = 'color';
                colorInput.className = 'manual-color-input ms-1';
                colorInput.value = '#000000';
                
                // 新增字體大小 input
                const fontSizeInput = document.createElement('input');
                fontSizeInput.type = 'number';
                fontSizeInput.className = 'manual-fontsize-input ms-1';
                fontSizeInput.value = 12;
                fontSizeInput.min = 8;
                fontSizeInput.max = 48;
                fontSizeInput.style.width = '48px';
                fontSizeInput.title = '字體大小';
                
                td.appendChild(input);
                td.appendChild(colorInput);
                td.appendChild(fontSizeInput);
                row.appendChild(td);
            });
            
            // 如果沒有列，自動創建第一列
            if (rows.length === 0) {
                addRowBtn.click();
            }
        });
        
        // 移除欄
        removeColumnBtn.addEventListener('click', function() {
            const thead = manualTable.querySelector('thead');
            const tbody = manualTable.querySelector('tbody');
            const headerRow = thead.querySelector('tr');
            const headers = headerRow.querySelectorAll('th');
            
            if (headers.length > 0) {
                // 移除最後一個表頭
                headerRow.removeChild(headers[headers.length - 1]);
                
                // 移除每一列的最後一個單元格
                const rows = tbody.querySelectorAll('tr');
                rows.forEach(row => {
                    const cells = row.querySelectorAll('td');
                    if (cells.length > 0) {
                        row.removeChild(cells[cells.length - 1]);
                    }
                });
            }
        });
    }
});

// 獲取手動插入的資料
function getManualInsertionData() {
    const manualTable = document.getElementById('manual-table');
    if (!manualTable) return { headers: [], rows: [] };
    
    const thead = manualTable.querySelector('thead');
    const tbody = manualTable.querySelector('tbody');
    const headers = [];
    const rows = [];
    
    // 獲取表頭
    if (thead) {
        thead.querySelectorAll('th').forEach(th => {
            headers.push(th.textContent.trim());
        });
    }
    
    // 獲取行數據
    if (tbody) {
        tbody.querySelectorAll('tr').forEach(tr => {
            const row = [];
            tr.querySelectorAll('td').forEach(td => {
                const input = td.querySelector('input.manual-input');
                const colorInput = td.querySelector('input.manual-color-input');
                const fontSizeInput = td.querySelector('input.manual-fontsize-input');
                row.push({
                    value: input ? input.value.trim() : '',
                    color: colorInput ? colorInput.value : '#000000',
                    fontSize: fontSizeInput ? parseInt(fontSizeInput.value) : 12
                });
            });
            if (row.some(cell => cell.value !== '')) {
                rows.push(row);
            }
        });
    }
    
    return { headers, rows };
} 