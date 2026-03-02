// 当前时间戳（毫秒）
const timestamp = Date.now();
pm.request.headers.upsert({ key: "Z-Timestamp", value: timestamp.toString() });

// HTTP 方法
const method = pm.request.method.toUpperCase();

// Path
const urlObj = pm.request.url;
const path = "/" + urlObj.path.join("/");

// Query string 原始顺序，不排序
const queryString = urlObj.query.all()
    .map(q => `${encodeURIComponent(q.key)}=${encodeURIComponent(q.value)}`)
    .join("&");

// 收集 X- 开头 headers（排除 X-Signature），按 key 排序，不加换行
let headersToSign = {};
pm.request.headers.each(header => {
    const key = header.key.toLowerCase();
    if (key.startsWith('x-') && key !== 'z-signature') {
        headersToSign[key] = header.value;
    }
});
const sortedHeaders = Object.keys(headersToSign)
    .sort()
    .map(k => `${k}:${headersToSign[k].trim()}`)
    .join('');

// Body
let bodyRaw = "";
if (pm.request.body && pm.request.body.mode === "raw") {
    try {
        const jsonObj = JSON.parse(pm.request.body.raw);
        // 最小化 JSON
        bodyRaw = JSON.stringify(jsonObj); // 默认就是 minified，没有空格
    } catch (e) {
        // 非 JSON 保持原始字符串
        bodyRaw = pm.request.body.raw;
    }
}

// 拼接 canonical string 与服务端一致
const canonical = method + path + "?" + queryString + bodyRaw + sortedHeaders;

// 获取 HMAC 密钥
const secretKey = pm.collectionVariables.get("HMAC_SECRET_KEY");
if (!secretKey) {
    throw new Error("HMAC_SECRET_KEY not set in collection variables");
}

// 计算 HMAC-SHA256
const CryptoJS = require('crypto-js');
const hmac = CryptoJS.HmacSHA256(canonical, secretKey).toString(CryptoJS.enc.Hex);

// 设置 X-Signature
pm.request.headers.upsert({ key: "Z-Signature", value: hmac });
