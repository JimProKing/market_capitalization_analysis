# step_1_3.py (진짜 진짜 최종판 – 2025.12.08 기준 완벽 동작)

import json
from pathlib import Path
from playwright.sync_api import Page, expect
from step_1_1 import OUT_DIR
from step_1_2 import run_playwright

OUT_1_3 = OUT_DIR / f"{Path(__file__).stem}.json"


def goto_market_cap(page: Page):
    # 코스피 시가총액 페이지 직접 이동
    page.goto("https://finance.naver.com/sise/sise_market_sum.naver", wait_until="networkidle")

    # 팝업/광고 닫기 (있으면 닫고 없으면 무시)
    for selector in ["a.btn_close", "button.close", "a.pop_close", "a.close"]:
        try:
            page.locator(selector).click(timeout=3000)
        except:
            pass


def parse_table_kospi(page: Page) -> tuple[list, list]:
    # 2025년 12월 현재 정확한 테이블 셀렉터
    table = page.locator("#contentarea > div.box_type_l > table.type_2")
    expect(table).to_be_visible(timeout=20000)

    # 헤더
    header = [th.inner_text().strip() for th in table.locator("thead th").all()]

    # 본문
    rows = table.locator("tbody > tr").all()
    body = []

    for row in rows:
        cells = row.locator("td").all()
        if len(cells) < 3:                    # 빈 행 스킵
            continue
        if any("코스피" in c.inner_text() or "코스닥" in c.inner_text() for c in cells):
            continue

        row_data = [c.inner_text().strip().replace("\n", " ").replace("\t", " ") for c in cells]
        body.append(row_data)

    return header, body


if __name__ == "__main__":
    playwright, browser, page = run_playwright(headless=False, slow_mo=800)  # 디버그용

    try:
        goto_market_cap(page)                     # ← 여기서 오타 고침!
        header, body = parse_table_kospi(page)

        result = {
            "header": header,
            "body": body,
            "total_count": len(body),
            "scraped_at": page.evaluate("() => new Date().toISOString()")
        }

        OUT_1_3.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"성공! {len(body)}개 종목 데이터 저장 완료 → {OUT_1_3}")

    except Exception as e:
        print("에러 발생:", e)
        page.screenshot(path="error_screenshot.png", full_page=True)
        print("스크린샷 저장됨: error_screenshot.png")
        raise
    finally:
        browser.close()
        playwright.stop()