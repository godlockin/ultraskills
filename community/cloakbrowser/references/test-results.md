# CloakBrowser 测试报告

> 测试时间: 2026-05-24
> 测试环境: macOS, headless 模式
> CloakBrowser 版本: 0.3.30 (Chromium 146)

## 测试对比: Playwright vs CloakBrowser

### Sannysoft Bot Detection (bot.sannysoft.com)

| 测试方案 | 通过项 | 失败项 | 通过率 |
|---------|-------|-------|-------|
| **Playwright 原生** | 19 | 11 | 63% |
| **Playwright + JS Stealth** | 26 | 4 | 87% |
| **CloakBrowser** | **31** | **0** | **100%** |

#### Playwright 原生失败项
- User Agent (Old)
- WebDriver (New)
- Chrome (New)
- Permissions (New)
- Plugins Length (Old)
- Plugins is of type PluginArray
- HEADCHR_UA
- HEADCHR_CHROME_OBJ
- HEADCHR_PERMISSIONS
- HEADCHR_IFRAME
- CHR_MEMORY

#### Playwright + Stealth 失败项
- WebDriver (New)
- Permissions (New)
- Plugins is of type PluginArray
- HEADCHR_PERMISSIONS

#### CloakBrowser 失败项
- 无 ✅

### BrowserLeaks WebDriver 检测

| 测试方案 | navigator.webdriver | 结果 |
|---------|-------------------|------|
| Playwright 原生 | `true` | ❌ 检测到自动化 |
| Playwright + Stealth | `undefined` | ⚠️ 隐藏但非标准值 |
| CloakBrowser | `false` | ✅ 与真实浏览器一致 |

### Navigator 属性对比

| 属性 | Playwright | CloakBrowser | 真实 Chrome |
|------|-----------|--------------|------------|
| `webdriver` | `true` | `false` | `false` |
| `plugins.length` | 0 | 5 | 3-5 |
| `hardwareConcurrency` | 真实值泄露 | 8 (伪装) | 真实值 |
| `chrome.runtime` | `undefined` | `undefined`* | `object` |

*注: `chrome.runtime` 需要扩展环境

## 结论

### CloakBrowser 优势

1. **100% Sannysoft 通过率** - 唯一全通过的方案
2. **源码级 webdriver=false** - 不可被 JS 层检测
3. **完整指纹伪装** - plugins、hardwareConcurrency 等
4. **API 兼容** - 直接替换 Playwright，无需改代码

### 适用场景

| 场景 | 推荐方案 |
|------|---------|
| 基础自动化测试 | Playwright 原生即可 |
| 轻度反爬站点 | Playwright + stealth 补丁 |
| reCAPTCHA/Cloudflare 保护站点 | **CloakBrowser** |
| 严格反爬 (DataDome, Kasada) | CloakBrowser + 住宅代理 + headed |

### 注意事项

- Cloudflare Turnstile 在 headless 模式仍需挑战，建议 `headless=False`
- 严格站点需配合住宅代理 (数据中心 IP 直接被拉黑)
- 启用 `geoip=True` 确保时区/语言与 IP 一致

## 测试脚本

测试脚本位置: `scripts/test_antibot_comparison.py`

```bash
# 运行完整测试
python3 scripts/test_antibot_comparison.py

# 运行进阶测试 (Cloudflare + Navigator 属性)
python3 scripts/test_antibot_advanced.py
```
