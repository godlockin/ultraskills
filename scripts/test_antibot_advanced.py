#!/usr/bin/env python3
"""
进阶测试: Cloudflare / DataDome 真实防护站点
"""

import asyncio
import json
from datetime import datetime

# 真实 Cloudflare 保护站点
CLOUDFLARE_SITES = [
    {
        "name": "nowsecure.nl (CF Turnstile)",
        "url": "https://nowsecure.nl/",
        "check_selector": "body",
        "success_text": ["passed", "success", "challenge"],
    },
    {
        "name": "cloudflare.com/cdn-cgi/trace",
        "url": "https://www.cloudflare.com/cdn-cgi/trace",
        "check_selector": "body",
        "success_text": ["fl="],  # 返回 trace 信息说明通过了
    },
]

async def test_cloudflare_playwright():
    """Playwright 原生测试 Cloudflare"""
    print("\n🎭 Playwright 原生 → Cloudflare")

    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for site in CLOUDFLARE_SITES:
            print(f"\n  → {site['name']}")
            try:
                response = await page.goto(site["url"], timeout=30000, wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)

                status = response.status if response else "N/A"
                body = await page.content()

                blocked = any(x in body.lower() for x in ["challenge", "captcha", "verify", "checking your browser"])
                passed = any(x in body for x in site["success_text"])

                print(f"    HTTP: {status} | Blocked: {blocked} | Content OK: {passed}")
                print(f"    Body preview: {body[:150]}...")

            except Exception as e:
                print(f"    ❌ {str(e)[:80]}")

        await browser.close()

async def test_cloudflare_cloakbrowser():
    """CloakBrowser 测试 Cloudflare"""
    print("\n🥷 CloakBrowser → Cloudflare")

    from cloakbrowser import launch_async

    browser = await launch_async(headless=True)
    page = await browser.new_page()

    for site in CLOUDFLARE_SITES:
        print(f"\n  → {site['name']}")
        try:
            response = await page.goto(site["url"], timeout=30000, wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)

            status = response.status if response else "N/A"
            body = await page.content()

            blocked = any(x in body.lower() for x in ["challenge", "captcha", "verify", "checking your browser"])
            passed = any(x in body for x in site["success_text"])

            print(f"    HTTP: {status} | Blocked: {blocked} | Content OK: {passed}")
            print(f"    Body preview: {body[:150]}...")

        except Exception as e:
            print(f"    ❌ {str(e)[:80]}")

    await browser.close()

async def test_navigator_checks():
    """详细对比 navigator 属性"""
    print("\n" + "="*60)
    print("🔍 Navigator 属性详细对比")
    print("="*60)

    check_script = """
        () => ({
            webdriver: navigator.webdriver,
            plugins_length: navigator.plugins?.length || 0,
            languages: navigator.languages,
            platform: navigator.platform,
            hardwareConcurrency: navigator.hardwareConcurrency,
            deviceMemory: navigator.deviceMemory,
            chrome_runtime: typeof window.chrome?.runtime,
            permissions_query: typeof navigator.permissions?.query,
        })
    """

    from playwright.async_api import async_playwright
    from cloakbrowser import launch_async

    print("\n📊 Playwright 原生:")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("about:blank")
        result = await page.evaluate(check_script)
        for k, v in result.items():
            status = "⚠️" if k == "webdriver" and v else "✅" if k == "webdriver" and not v else ""
            print(f"  {k}: {v} {status}")
        await browser.close()

    print("\n📊 CloakBrowser:")
    browser = await launch_async(headless=True)
    page = await browser.new_page()
    await page.goto("about:blank")
    result = await page.evaluate(check_script)
    for k, v in result.items():
        status = "✅" if k == "webdriver" and not v else ""
        print(f"  {k}: {v} {status}")
    await browser.close()

async def main():
    print(f"🔬 进阶反爬测试 - Cloudflare & Navigator 属性")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    await test_navigator_checks()
    await test_cloudflare_playwright()
    await test_cloudflare_cloakbrowser()

    print("\n" + "="*60)
    print("✅ 测试完成")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())
