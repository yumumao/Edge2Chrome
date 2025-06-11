
console.log("Test extension loaded");

chrome.runtime.onInstalled.addListener(() => {
    console.log("Test extension installed");
    
    // 测试Native Host连接
    try {
        const port = chrome.runtime.connectNative('com.edge2chrome.launcher');
        
        port.onMessage.addListener((response) => {
            console.log("Native Host响应:", response);
        });
        
        port.onDisconnect.addListener(() => {
            console.log("Native Host断开连接");
            if (chrome.runtime.lastError) {
                console.error("连接错误:", chrome.runtime.lastError);
            }
        });
        
        // 发送测试消息
        const testMessage = {
            url: "https://www.zhihu.com/test-from-extension",
            source: "test-extension",
            chromeArgs: "--new-window",
            timestamp: Date.now()
        };
        
        console.log("发送测试消息:", testMessage);
        port.postMessage(testMessage);
        
    } catch (error) {
        console.error("连接Native Host失败:", error);
    }
});
