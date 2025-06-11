// Edge2Chrome Options Script

// 默认设置
const defaultSettings = {
    urlRules: ['*.zhihu.*'],
    showNotifications: true,
    enableLogging: false,
    buttonText: 'Chrome',
    chromeArgs: '--new-window'
};

// 加载设置
async function loadSettings() {
    try {
        const settings = await chrome.storage.sync.get(defaultSettings);
        
        // 更新UI
        document.getElementById('showNotifications').checked = settings.showNotifications;
        document.getElementById('enableLogging').checked = settings.enableLogging;
        document.getElementById('buttonText').value = settings.buttonText;
        document.getElementById('chromeArgs').value = settings.chromeArgs;
        
        // 加载规则列表
        updateRulesList(settings.urlRules);
        
        console.log('[Edge2Chrome] 设置已加载:', settings);
    } catch (error) {
        console.error('[Edge2Chrome] 加载设置失败:', error);
        showErrorMessage('设置加载失败');
    }
}

// 更新规则列表显示
function updateRulesList(rules) {
    const rulesList = document.getElementById('rulesList');
    rulesList.innerHTML = '';
    
    if (!rules || rules.length === 0) {
        rulesList.innerHTML = '<li style="padding: 10px; color: #666; text-align: center;">暂无规则</li>';
        return;
    }
    
    rules.forEach((rule, index) => {
        const li = document.createElement('li');
        li.className = 'rule-item';
        li.innerHTML = `
            <span class="rule-text">${escapeHtml(rule)}</span>
            <button class="delete-rule" data-index="${index}">删除</button>
        `;
        rulesList.appendChild(li);
    });
}

// HTML转义函数
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 通配符匹配函数
function wildcardMatch(pattern, text) {
    try {
        const regex = new RegExp(
            '^' + pattern.replace(/\*/g, '.*').replace(/\?/g, '.') + '$',
            'i'
        );
        return regex.test(text);
    } catch (e) {
        console.error('[Edge2Chrome] 正则表达式错误:', e);
        return false;
    }
}

// 测试URL匹配
async function testUrlMatch() {
    const testUrl = document.getElementById('testUrl').value.trim();
    const testResult = document.getElementById('testResult');
    
    if (!testUrl) {
        testResult.textContent = '请输入URL';
        testResult.className = 'test-no-match';
        return;
    }
    
    try {
        const settings = await chrome.storage.sync.get(['urlRules']);
        const rules = settings.urlRules || defaultSettings.urlRules;
        
        const matchedRules = rules.filter(rule => wildcardMatch(rule, testUrl));
        
        if (matchedRules.length > 0) {
            testResult.textContent = `✅ 匹配成功！匹配的规则: ${matchedRules.join(', ')}`;
            testResult.className = 'test-match';
        } else {
            testResult.textContent = `❌ 无匹配规则，此URL不会用Chrome打开`;
            testResult.className = 'test-no-match';
        }
    } catch (error) {
        console.error('[Edge2Chrome] 测试匹配失败:', error);
        testResult.textContent = '测试失败';
        testResult.className = 'test-no-match';
    }
}

// 添加规则
async function addRule() {
    const urlInput = document.getElementById('urlInput');
    const newRule = urlInput.value.trim();
    
    if (!newRule) {
        showErrorMessage('请输入URL规则');
        return;
    }
    
    // 简单验证规则格式
    if (newRule.length < 3) {
        showErrorMessage('规则太短，请输入有效的URL模式');
        return;
    }
    
    try {
        const settings = await chrome.storage.sync.get(['urlRules']);
        const rules = settings.urlRules || defaultSettings.urlRules;
        
        if (rules.includes(newRule)) {
            showErrorMessage('此规则已存在');
            return;
        }
        
        rules.push(newRule);
        await chrome.storage.sync.set({ urlRules: rules });
        
        updateRulesList(rules);
        urlInput.value = '';
        
        showSuccessMessage('规则添加成功');
    } catch (error) {
        console.error('[Edge2Chrome] 添加规则失败:', error);
        showErrorMessage('添加规则失败');
    }
}

// 删除规则
async function deleteRule(index) {
    try {
        const settings = await chrome.storage.sync.get(['urlRules']);
        const rules = settings.urlRules || defaultSettings.urlRules;
        
        if (index >= 0 && index < rules.length) {
            const deletedRule = rules[index];
            rules.splice(index, 1);
            await chrome.storage.sync.set({ urlRules: rules });
            
            updateRulesList(rules);
            showSuccessMessage(`规则 "${deletedRule}" 删除成功`);
        }
    } catch (error) {
        console.error('[Edge2Chrome] 删除规则失败:', error);
        showErrorMessage('删除规则失败');
    }
}

// 保存设置
async function saveSettings() {
    try {
        const currentRules = (await chrome.storage.sync.get(['urlRules'])).urlRules || defaultSettings.urlRules;
        
        const settings = {
            urlRules: currentRules,
            showNotifications: document.getElementById('showNotifications').checked,
            enableLogging: document.getElementById('enableLogging').checked,
            buttonText: document.getElementById('buttonText').value.trim() || defaultSettings.buttonText,
            chromeArgs: document.getElementById('chromeArgs').value.trim() || defaultSettings.chromeArgs
        };
        
        await chrome.storage.sync.set(settings);
        showSuccessMessage('设置保存成功');
        
        console.log('[Edge2Chrome] 设置已保存:', settings);
    } catch (error) {
        console.error('[Edge2Chrome] 保存设置失败:', error);
        showErrorMessage('保存设置失败');
    }
}

// 重置设置
async function resetSettings() {
    if (confirm('确定要重置所有设置为默认值吗？这将删除所有自定义规则。')) {
        try {
            await chrome.storage.sync.clear();
            await chrome.storage.sync.set(defaultSettings);
            await loadSettings();
            showSuccessMessage('设置已重置为默认值');
        } catch (error) {
            console.error('[Edge2Chrome] 重置设置失败:', error);
            showErrorMessage('重置设置失败');
        }
    }
}

// 导出设置
async function exportSettings() {
    try {
        const settings = await chrome.storage.sync.get();
        const dataStr = JSON.stringify(settings, null, 2);
        const blob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `edge2chrome-settings-${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        
        URL.revokeObjectURL(url);
        showSuccessMessage('设置已导出');
    } catch (error) {
        console.error('[Edge2Chrome] 导出设置失败:', error);
        showErrorMessage('导出设置失败');
    }
}

// 导入设置
function importSettings() {
    document.getElementById('importFile').click();
}

// 处理文件导入
async function handleFileImport(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    try {
        const text = await file.text();
        const settings = JSON.parse(text);
        
        // 验证设置格式
        if (!settings.urlRules || !Array.isArray(settings.urlRules)) {
            throw new Error('无效的设置文件格式：缺少urlRules数组');
        }
        
        // 合并设置，保留默认值
        const mergedSettings = { ...defaultSettings, ...settings };
        
        await chrome.storage.sync.set(mergedSettings);
        await loadSettings();
        showSuccessMessage('设置导入成功');
        
        // 清空文件输入
        event.target.value = '';
    } catch (error) {
        console.error('[Edge2Chrome] 导入失败:', error);
        showErrorMessage(`导入失败: ${error.message}`);
    }
}

// 显示成功消息
function showSuccessMessage(message) {
    showMessage(message, 'success');
}

// 显示错误消息  
function showErrorMessage(message) {
    showMessage(message, 'error');
}

// 显示消息
function showMessage(message, type) {
    // 移除已存在的消息
    const existing = document.querySelector('.success-message, .error-message');
    if (existing) {
        existing.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = type === 'success' ? 'success-message' : 'error-message';
    messageDiv.textContent = message;
    
    // 为错误消息添加样式
    if (type === 'error') {
        messageDiv.style.background = '#f8d7da';
        messageDiv.style.color = '#721c24';
        messageDiv.style.border = '1px solid #f5c6cb';
    }
    
    document.querySelector('.container').appendChild(messageDiv);
    
    setTimeout(() => {
        messageDiv.remove();
    }, 3000);
}

// 事件监听器
document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
    
    // 规则管理
    document.getElementById('addRule').addEventListener('click', addRule);
    document.getElementById('urlInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addRule();
    });
    
    document.getElementById('rulesList').addEventListener('click', (e) => {
        if (e.target.classList.contains('delete-rule')) {
            const index = parseInt(e.target.dataset.index);
            deleteRule(index);
        }
    });
    
    // 设置管理
    document.getElementById('saveSettings').addEventListener('click', saveSettings);
    document.getElementById('resetSettings').addEventListener('click', resetSettings);
    document.getElementById('exportSettings').addEventListener('click', exportSettings);
    document.getElementById('importSettings').addEventListener('click', importSettings);
    document.getElementById('importFile').addEventListener('change', handleFileImport);
    
    // 测试工具
    document.getElementById('testMatch').addEventListener('click', testUrlMatch);
    document.getElementById('testUrl').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') testUrlMatch();
    });
    
    // 模板按钮事件
    document.querySelectorAll('.template-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.getElementById('urlInput').value = btn.dataset.rule;
        });
    });
});