#!/usr/bin/env python3
"""
反爬能力对比测试: CloakBrowser vs Playwright (原生)
测试站点:
1. bot.sannysoft.com - 综合 bot 检测
2. browserleaks.com/webdriver - WebDriver 检测
3. nowsecure.nl - Cloudflare 检测
"""

import asyncio
import json
import time
from datetime import datetime

# ============ Test Sites ============
TEST_SITES = [
    {
        "name": "Sannysoft Bot Detection",
        "url": "https://bot.sannysoft.com/",
        "check": "sannysoft",
    },
    {
        "name": "BrowserLeaks WebDriver",
        "url": "https://browserleaks.com/webdriver",
        "check": "browserleaks",
    },
    {
        "name": "CreepJS Fingerprint",
        "url": "https://abrahamjuliot.github.io/creepjs/",
        "check": "creepjs",
    },
]

async def check_sannysoft(page) -> dict:
    """检查 sannysoft 测试结果"""
    await page.wait_for_timeout(3000)

    # 获取失败项
    failed = await page.eval_on_selector_all(
        "td.failed",
        "els => els.map(e => e.parentElement?.querySelector('td')?.textContent || 'unknown')"
    )

    # 获取通过项数量
    passed = await page.eval_on_selector_all(
        "td.passed",
        "els => els.length"
    )

    return {
        "passed": passed if isinstance(passed, int) else len(passed) if passed else 0,
        "failed": failed if failed else [],
        "score": f"{passed}/{passed + len(failed)}" if passed else "N/A"
    }

async def check_browserleaks(page) -> dict:
    """检查 browserleaks webdriver 检测"""
    await page.wait_for_timeout(2000)

    try:
        # 检查 webdriver 状态
        webdriver_status = await page.evaluate("""
            () => {
                const el = document.querySelector('#webdriver-result, .result');
                return el ? el.textContent : navigator.webdriver?.toString() || 'unknown';
            }
        """)

        return {
            "webdriver_detected": "true" in str(webdriver_status).lower(),
            "raw": webdriver_status[:200] if webdriver_status else "N/A"
        }
    except Exception as e:
        return {"error": str(e)}

async def check_creepjs(page) -> dict:
    """检查 CreepJS 指纹分析"""
    await page.wait_for_timeout(5000)  # CreepJS 需要更长加载时间

    try:
        # 获取信任分数
        result = await page.evaluate("""
            () => {
                const trustScore = document.querySelector('.trust-score, [class*="trust"]');
                const botStatus = document.querySelector('[class*="bot"], [class*="lie"]');
                return {
                    trust: trustScore?.textContent || 'N/A',
                    bot: botStatus?.textContent || 'N/A'
                };
            }
        """)
        return result
    except Exception as e:
        return {"error": str(e)}

async def test_playwright_native():
    """测试原生 Playwright"""
    print("\n" + "="*60)
    print("🎭 测试: Playwright (原生 headless)")
    print("="*60)

    from playwright.async_api import async_playwright

    results = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        for site in TEST_SITES:
            print(f"\n→ {site['name']}...")
            try:
                await page.goto(site["url"], timeout=30000)

                if site["check"] == "sannysoft":
                    result = await check_sannysoft(page)
                elif site["check"] == "browserleaks":
                    result = await check_browserleaks(page)
                elif site["check"] == "creepjs":
                    result = await check_creepjs(page)
                else:
                    result = {"status": "loaded"}

                results[site["name"]] = result
                print(f"  结果: {json.dumps(result, ensure_ascii=False)[:100]}")

            except Exception as e:
                results[site["name"]] = {"error": str(e)[:100]}
                print(f"  ❌ 错误: {str(e)[:100]}")

        await browser.close()

    return results

async def test_cloakbrowser():
    """测试 CloakBrowser"""
    print("\n" + "="*60)
    print("🥷 测试: CloakBrowser (stealth)")
    print("="*60)

    from cloakbrowser import launch_async

    results = {}

    browser = await launch_async(headless=True)
    page = await browser.new_page()

    for site in TEST_SITES:
        print(f"\n→ {site['name']}...")
        try:
            await page.goto(site["url"], timeout=30000)

            if site["check"] == "sannysoft":
                result = await check_sannysoft(page)
            elif site["check"] == "browserleaks":
                result = await check_browserleaks(page)
            elif site["check"] == "creepjs":
                result = await check_creepjs(page)
            else:
                result = {"status": "loaded"}

            results[site["name"]] = result
            print(f"  结果: {json.dumps(result, ensure_ascii=False)[:100]}")

        except Exception as e:
            results[site["name"]] = {"error": str(e)[:100]}
            print(f"  ❌ 错误: {str(e)[:100]}")

    await browser.close()

    return results

async def test_playwright_stealth():
    """测试 Playwright + stealth 补丁"""
    print("\n" + "="*60)
    print("🎭+🛡️ 测试: Playwright + Stealth 补丁")
    print("="*60)

    from playwright.async_api import async_playwright

    results = {}

    STEALTH_SCRIPT = """
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        Object.defineProperty(navigator, 'plugins', {
            get: () => [
                { name: 'Chrome PDF Plugin' },
                { name: 'Chrome PDF Viewer' },
                { name: 'Native Client' },
            ]
        });
        Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
        window.chrome = { runtime: {} };
    """

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        await context.add_init_script(STEALTH_SCRIPT)
        page = await context.new_page()

        for site in TEST_SITES:
            print(f"\n→ {site['name']}...")
            try:
                await page.goto(site["url"], timeout=30000)

                if site["check"] == "sannysoft":
                    result = await check_sannysoft(page)
                elif site["check"] == "browserleaks":
                    result = await check_browserleaks(page)
                elif site["check"] == "creepjs":
                    result = await check_creepjs(page)
                else:
                    result = {"status": "loaded"}

                results[site["name"]] = result
                print(f"  结果: {json.dumps(result, ensure_ascii=False)[:100]}")

            except Exception as e:
                results[site["name"]] = {"error": str(e)[:100]}
                print(f"  ❌ 错误: {str(e)[:100]}")

        await browser.close()

    return results

def print_comparison(pw_results, cloak_results, stealth_results):
    """打印对比表"""
    print("\n" + "="*80)
    print("📊 对比结果")
    print("="*80)

    print(f"\n{'测试项':<30} {'Playwright':<20} {'PW+Stealth':<20} {'CloakBrowser':<20}")
    print("-"*90)

    for site in TEST_SITES:
        name = site["name"]
        pw = pw_results.get(name, {})
        stealth = stealth_results.get(name, {})
        cloak = cloak_results.get(name, {})

        # 简化显示
        pw_str = _format_result(pw)
        stealth_str = _format_result(stealth)
        cloak_str = _format_result(cloak)

        print(f"{name:<30} {pw_str:<20} {stealth_str:<20} {cloak_str:<20}")

def _format_result(result):
    if "error" in result:
        return "❌ Error"
    if "score" in result:
        failed = len(result.get("failed", []))
        return f"{'✅' if failed == 0 else '⚠️'} {result['score']} ({failed} fail)"
    if "webdriver_detected" in result:
        return "❌ Detected" if result["webdriver_detected"] else "✅ Hidden"
    if "trust" in result:
        return f"Trust: {result['trust'][:10]}"
    return str(result)[:15]

async def main():
    print(f"\n🔬 反爬能力对比测试")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试站点: {len(TEST_SITES)} 个")

    # 运行测试
    pw_results = await test_playwright_native()
    stealth_results = await test_playwright_stealth()
    cloak_results = await test_cloakbrowser()

    # 打印对比
    print_comparison(pw_results, cloak_results, stealth_results)

    # 保存详细结果
    full_results = {
        "timestamp": datetime.now().isoformat(),
        "playwright_native": pw_results,
        "playwright_stealth": stealth_results,
        "cloakbrowser": cloak_results,
    }

    with open("antibot_test_results.json", "w") as f:
        json.dump(full_results, f, indent=2, ensure_ascii=False)

    print(f"\n📁 详细结果已保存到: antibot_test_results.json")

if __name__ == "__main__":
    asyncio.run(main())
