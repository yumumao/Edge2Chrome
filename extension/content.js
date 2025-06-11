// Edge2Chrome Content Script
let currentSettings = null;

const defaultSettings = {
  urlRules: ['*.zhihu.*'],
  showNotifications: true,
  enableLogging: false,
  buttonText: 'Chrome',
  chromeArgs: '--new-window'
};

async function loadSettings() {
  try {
    currentSettings = await chrome.storage.sync.get(defaultSettings);
    log('设置已加载:', currentSettings);
  } catch (error) {
    console.error('[Edge2Chrome] 加载设置失败:', error);
    currentSettings = defaultSettings;
  }
}

function log(...args) {
  if (currentSettings && currentSettings.enableLogging) {
    console.log('[Edge2Chrome]', ...args);
  }
}

function wildcardMatch(pattern, text) {
  try {
    const regex = new RegExp(
      '^' + pattern.replace(/\*/g, '.*').replace(/\?/g, '.') + '$',
      'i'
    );
    return regex.test(text);
  } catch (e) {
    log('正则表达式错误:', e);
    return false;
  }
}

function shouldOpenInChrome(url) {
  if (!currentSettings || !currentSettings.urlRules || !Array.isArray(currentSettings.urlRules)) {
    return false;
  }
  
  try {
    return currentSettings.urlRules.some(rule => wildcardMatch(rule, url));
  } catch (e) {
    log('URL匹配错误:', e);
    return false;
  }
}

function addChromeButtons() {
  if (!currentSettings) return;
  
  const links = document.querySelectorAll('a[href]');
  let addedCount = 0;
  
  links.forEach(link => {
    const href = link.href;
    
    if (!href || href.startsWith('javascript:') || href.startsWith('mailto:') || href.startsWith('tel:')) {
      return;
    }
    
    if (shouldOpenInChrome(href) && !link.dataset.edge2chromeAdded) {
      link.dataset.edge2chromeAdded = 'true';
      
      const chromeBtn = document.createElement('span');
      chromeBtn.className = 'edge2chrome-btn';
      chromeBtn.innerHTML = `🌐 ${currentSettings.buttonText}`;
      chromeBtn.title = `用Chrome打开: ${href}`;
      
      chromeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        
        log('准备用Chrome打开:', href);
        
        chrome.runtime.sendMessage({
          action: 'openInChrome',
          url: href,
          chromeArgs: currentSettings.chromeArgs
        }).then((response) => {
          if (response && response.success) {
            log('✅ 成功发送到Chrome');
            if (currentSettings.showNotifications) {
              showNotification('已用Chrome打开链接', 'success');
            }
          } else {
            const errorMsg = response ? response.error : '未知错误';
            log('❌ 发送失败:', errorMsg);
            if (currentSettings.showNotifications) {
              showNotification(`打开失败: ${errorMsg}`, 'error');
            }
            
            console.error('[Edge2Chrome] 详细错误信息:', {
              url: href,
              response: response,
              currentSettings: currentSettings
            });
          }
        }).catch((error) => {
          log('❌ 通信错误:', error);
          if (currentSettings.showNotifications) {
            showNotification(`扩展通信错误: ${error.message}`, 'error');
          }
          
          console.error('[Edge2Chrome] 通信异常:', error);
        });
      });
      
      link.style.position = 'relative';
      link.appendChild(chromeBtn);
      addedCount++;
    }
  });
  
  if (addedCount > 0) {
    log(`添加了 ${addedCount} 个Chrome按钮`);
  }
}

function showNotification(message, type = 'info') {
  if (!currentSettings || !currentSettings.showNotifications) return;
  
  const existingNotification = document.querySelector('.edge2chrome-notification');
  if (existingNotification) {
    existingNotification.remove();
  }
  
  const notification = document.createElement('div');
  notification.className = `edge2chrome-notification edge2chrome-notification-${type}`;
  notification.textContent = message;
  
  document.body.appendChild(notification);
  
  setTimeout(() => {
    if (notification.parentNode) {
      notification.parentNode.removeChild(notification);
    }
  }, 3000);
}

chrome.storage.onChanged.addListener((changes, namespace) => {
  if (namespace === 'sync') {
    log('设置已更改，重新加载...');
    loadSettings().then(() => {
      document.querySelectorAll('[data-edge2chrome-added]').forEach(link => {
        link.removeAttribute('data-edge2chrome-added');
        const btn = link.querySelector('.edge2chrome-btn');
        if (btn) btn.remove();
      });
      addChromeButtons();
    });
  }
});

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

loadSettings().then(() => {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addChromeButtons);
  } else {
    addChromeButtons();
  }
  
  const debouncedAddButtons = debounce(addChromeButtons, 200);
  
  const observer = new MutationObserver((mutations) => {
    let shouldCheck = false;
    
    mutations.forEach((mutation) => {
      if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
        for (let node of mutation.addedNodes) {
          if (node.nodeType === Node.ELEMENT_NODE) {
            if (node.tagName === 'A' || node.querySelector('a')) {
              shouldCheck = true;
              break;
            }
          }
        }
      }
    });
    
    if (shouldCheck) {
      debouncedAddButtons();
    }
  });
  
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
});