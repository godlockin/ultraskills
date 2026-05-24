# CloakBrowser 反检测原理

## 为什么 JS 注入/配置补丁不够？

### 检测层级

```
┌─────────────────────────────────────────────────────────┐
│  Level 4: 行为分析                                        │
│  鼠标轨迹、打字节奏、滚动模式、阅读时间                      │
├─────────────────────────────────────────────────────────┤
│  Level 3: 指纹深度检测 (FingerprintJS, BrowserScan)        │
│  Canvas/WebGL/Audio 哈希、字体枚举、存储配额                 │
├─────────────────────────────────────────────────────────┤
│  Level 2: Navigator/Window 属性                           │
│  webdriver, plugins, languages, chrome.runtime           │
├─────────────────────────────────────────────────────────┤
│  Level 1: 基础检测                                        │
│  User-Agent, HTTP 头, TLS 指纹                           │
└─────────────────────────────────────────────────────────┘
```

### 各层解决方案对比

| 层级 | playwright-stealth | undetected-chromedriver | CloakBrowser |
|------|-------------------|------------------------|--------------|
| L1 基础 | ✅ UA 覆盖 | ✅ UA 覆盖 | ✅ 源码级 |
| L2 属性 | ⚠️ JS 覆盖 (可被检测) | ⚠️ 配置补丁 | ✅ 源码级 |
| L3 指纹 | ❌ 无法完全覆盖 | ❌ 无法完全覆盖 | ✅ 源码级 |
| L4 行为 | ❌ 无 | ❌ 无 | ✅ humanize |

## CloakBrowser 58 个源码补丁覆盖范围

### 自动化信号移除
- `navigator.webdriver` → `false` (C++ 层)
- CDP 自动化检测信号
- Playwright/Puppeteer 特有属性

### 指纹伪装
- Canvas 渲染噪声注入
- WebGL 渲染器/厂商字符串
- Audio 上下文指纹
- 字体枚举结果
- GPU/硬件参数
- 屏幕/窗口尺寸
- 存储配额

### 网络层
- TLS 指纹 (ja3n/ja4 匹配真实 Chrome)
- 代理信号移除 (DNS/连接时序归零)
- WebRTC IP 泄漏防护

### 行为层 (humanize=True)
- 贝塞尔曲线鼠标移动
- 变速打字 + 偶尔打错
- 渐进式滚动
- 动作间微移动

## 为什么 JS 覆盖会被检测？

```javascript
// 典型的 JS stealth 补丁
Object.defineProperty(navigator, 'webdriver', { get: () => false });

// 反检测脚本可以检查：
// 1. 属性描述符是否被修改
Object.getOwnPropertyDescriptor(navigator, 'webdriver');

// 2. 原型链是否被污染
navigator.__proto__.webdriver;

// 3. 时序差异 (JS 覆盖有微秒级延迟)
```

CloakBrowser 在 Chromium 源码中直接修改返回值，**不存在上述检测向量**。

## reCAPTCHA v3 评分机制

Google reCAPTCHA v3 使用机器学习评估用户可信度：

| 信号类型 | 权重 | CloakBrowser 对策 |
|---------|------|------------------|
| CDP 协议活动 | 高 | 源码级移除 |
| 鼠标轨迹熵 | 高 | humanize 贝塞尔曲线 |
| 打字节奏 | 中 | humanize 变速 |
| navigator.webdriver | 中 | 源码级 false |
| Canvas 指纹一致性 | 中 | 固定 seed 跨会话 |
| IP 信誉 | 高 | 需配合住宅代理 |

### 最佳配置

```python
browser = launch(
    proxy="socks5://residential:port",
    geoip=True,
    humanize=True,
    args=["--fingerprint=YOUR_FIXED_SEED"],  # 重复访问用固定身份
)
```

## Cloudflare Turnstile 工作原理

Turnstile 综合检测：
1. **JavaScript 挑战** - 执行计算密集型代码
2. **环境检测** - 检查自动化信号
3. **行为分析** - 鼠标/键盘模式 (managed 模式)
4. **机器学习评分** - 历史行为模式

### CloakBrowser 通过策略

- **非交互模式**: 自动通过 (环境检测过关)
- **托管模式**: 单击通过 (行为检测 + humanize)
- **交互模式**: 需手动解决 (CAPTCHA)

## 检测绕过最佳实践

### DO ✅

```python
# 1. 用原生 sleep 而不是 Playwright timeout
import time
time.sleep(3)

# 2. 用 type() 而不是 fill()
page.type("#input", "text", delay=50)

# 3. 住宅代理 + geoip
launch(proxy="socks5://...", geoip=True)

# 4. 重复访问同一站点用固定指纹
launch(args=["--fingerprint=12345"])
```

### DON'T ❌

```python
# 1. 不要用 wait_for_timeout (发送 CDP 命令)
page.wait_for_timeout(3000)  # ❌

# 2. 不要用数据中心 IP
launch(proxy="http://datacenter-proxy:8080")  # ❌

# 3. 不要频繁切换指纹
launch()  # 每次随机指纹 - 对重复访问不利
```

## 参考资源

- [FingerprintJS 检测原理](https://fingerprint.com/blog/browser-fingerprinting-techniques/)
- [Cloudflare Bot Management](https://blog.cloudflare.com/introducing-bot-analytics/)
- [reCAPTCHA v3 评分系统](https://developers.google.com/recaptcha/docs/v3)
