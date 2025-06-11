// Edge2Chrome Background Script (Edge终极适配版)
console.log('[Edge2Chrome] 终极适配版Background Script启动');

// 处理来自content script的消息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('[Edge2Chrome] 收到请求:', request);
  
  if (request.action === 'openInChrome') {
    handleChromeRequest(request, sendResponse);
    return true; // 保持异步通道开启
  }
  
  return false;
});

function handleChromeRequest(request, sendResponse) {
  console.log('[Edge2Chrome] 处理Chrome请求:', request.url);
  
  // 立即响应避免超时
  let responseHandled = false;
  
  try {
    console.log('[Edge2Chrome] 创建Native Host连接...');
    
    // 创建Native Host连接
    const nativePort = chrome.runtime.connectNative('com.edge2chrome.launcher');
    
    // 连接超时保护
    const connectionTimeout = setTimeout(() => {
      if (!responseHandled) {
        console.error('[Edge2Chrome] Native Host连接超时');
        responseHandled = true;
        
        try {
          nativePort.disconnect();
        } catch (e) {}
        
        sendResponse({
          success: false,
          error: 'Native Host连接超时'
        });
      }
    }, 3000); // 减少到3秒
    
    // 监听响应
    nativePort.onMessage.addListener((response) => {
      console.log('[Edge2Chrome] 收到Native Host响应:', response);
      
      if (!responseHandled) {
        responseHandled = true;
        clearTimeout(connectionTimeout);
        
        // 立即发送响应
        sendResponse({
          success: true,
          response: response
        });
        
        // 断开连接
        try {
          nativePort.disconnect();
        } catch (e) {
          console.log('[Edge2Chrome] 断开连接时出错:', e);
        }
      }
    });
    
    // 监听连接断开
    nativePort.onDisconnect.addListener(() => {
      console.log('[Edge2Chrome] Native Host连接断开');
      clearTimeout(connectionTimeout);
      
      if (!responseHandled) {
        responseHandled = true;
        
        let errorMessage = 'Native Host连接断开';
        
        if (chrome.runtime.lastError) {
          console.error('[Edge2Chrome] 连接错误:', chrome.runtime.lastError);
          errorMessage = `连接失败: ${chrome.runtime.lastError.message}`;
        }
        
        sendResponse({
          success: false,
          error: errorMessage
        });
      }
    });
    
    // 构造消息
    const message = {
      url: request.url,
      source: 'edge-ultimate',
      chromeArgs: request.chromeArgs || '--new-window',
      timestamp: Date.now()
    };
    
    console.log('[Edge2Chrome] 发送消息到Native Host:', message);
    
    // 发送消息
    nativePort.postMessage(message);
    
  } catch (error) {
    console.error('[Edge2Chrome] 连接异常:', error);
    
    if (!responseHandled) {
      responseHandled = true;
      sendResponse({
        success: false,
        error: `连接异常: ${error.message}`
      });
    }
  }
}

// 扩展生命周期事件
chrome.runtime.onInstalled.addListener((details) => {
  console.log('[Edge2Chrome] 扩展安装/更新:', details.reason);
});

console.log('[Edge2Chrome] 终极适配版Background Script加载完成');