# step_1_2.py (최종 추천 버전)

from playwright.sync_api import sync_playwright, Playwright, Browser, Page

def run_playwright(
    headless: bool = True,
    slow_mo: int = 0,
    viewport: dict | None = None,
) -> tuple[Playwright, Browser, Browser, Page]:
    playwright = sync_playwright().start()
    
    browser = playwright.chromium.launch(
        headless=headless,
        slow_mo=slow_mo,
    )
    
    context = browser.new_context(
        viewport=viewport or {"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    )
    
    page = context.new_page()
    return playwright, browser, page