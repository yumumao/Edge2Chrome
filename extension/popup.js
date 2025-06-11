// Edge2Chrome Popup Script

document.addEventListener('DOMContentLoaded', async () => {
    const quickRule = document.getElementById('quickRule');
    const addQuickRule = document.getElementById('addQuickRule');
    const openSettings = document.getElementById('openSettings');
    const testCurrent = document.getElementById('testCurrent');
    const status = document.getElementById('status');
    const ruleCount = document.getElementById('ruleCount');
    
    // 显示状态消息
    function showStatus(message, type = 'success') {
        status.textContent = message;
        status.className = `status ${type}`;
        status.style.display = 'block';
        setTimeout(() => {
            status.style.display = 'none';
        }, 2500);
    }
    
    // 通配符匹配函数
    function wildcardMatch(pattern, text) {
        try {
            const regex = new RegExp('^' + pattern.replace(/\*/g, '.*').replace(/\?/g, '.') + '$', 'i');
            return regex.test(text);
        } catch (e) {
            return false;
        }
    }
    
    // 加载并显示当前规则数量
    async function loadRuleCount() {
        try {
            const settings = await chrome.storage.sync.get(['urlRules']);
            const rules = settings.urlRules || ['*.zhihu.*'];
            ruleCount.textContent = `共 ${rules.length} 条规则`;
        } catch (error) {
            ruleCount.textContent = '加载失败';
        }
    }
    
    // 初始加载
    await loadRuleCount();
    
    // 快速添加规则
    addQuickRule.addEventListener('click', async () => {
        const rule = quickRule.value.trim();
        if (!rule) {
            showStatus('请输入规则', 'error');
            return;
        }
        
        if (rule.length < 3) {
            showStatus('规则太短', 'error');
            return;
        }
        
        try {
            const settings = await chrome.storage.sync.get(['urlRules']);
            const rules = settings.urlRules || ['*.zhihu.*'];
            
            if (rules.includes(rule)) {
                showStatus('规则已存在', 'error');
                return;
            }
            
            rules.push(rule);
            await chrome.storage.sync.set({ urlRules: rules });
            quickRule.value = '';
            showStatus('规则添加成功');
            await loadRuleCount();
        } catch (error) {
            console.error('[Edge2Chrome] 添加规则失败:', error);
            showStatus('添加失败', 'error');
        }
    });
    
    // 回车键快速添加
    quickRule.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addQuickRule.click();
        }
    });
    
    // 打开设置页面
    openSettings.addEventListener('click', () => {
        chrome.runtime.openOptionsPage();
        window.close();
    });
    
    // 测试当前页面
    testCurrent.addEventListener('click', async () => {
        try {
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            const settings = await chrome.storage.sync.get(['urlRules']);
            const rules = settings.urlRules || ['*.zhihu.*'];
            
            const matchedRules = rules.filter(rule => wildcardMatch(rule, tab.url));
            
            if (matchedRules.length > 0) {
                showStatus(`✅ 匹配 ${matchedRules.length} 条规则`);
            } else {
                showStatus('❌ 无匹配规则', 'error');
            }
        } catch (error) {
            console.error('[Edge2Chrome] 测试当前页面失败:', error);
            showStatus('测试失败', 'error');
        }
    });
});