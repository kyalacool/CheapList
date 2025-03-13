from playwright.sync_api import sync_playwright

def get_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Automatically downloads Chromium if needed
        page = browser.new_page()
        page.goto(url)
        try:
            page.wait_for_selector("button:has-text('Mindennek a megengedése')", timeout=5000)
            page.click("button:has-text('Mindennek a megengedése')")
            print("Cookie consent accepted.")
        except Exception as e:
            print("Cookie consent button not found or click failed:", e)
        try:
            while True:
                # Find all "Show More" buttons (adjust the selector as needed)
                buttons = page.locator("span:has-text('További')")

                # Check if any button exists
                count = buttons.count()
                if count == 0:
                    print("No more 'További termék megjelenítésee' buttons found.")
                    break

                # Click all available buttons
                for i in range(count):
                    buttons.nth(i).click()
                    page.wait_for_timeout(1000)  # Small delay to allow loading

                print(f"Clicked {count} 'További termék megjelenítése' button(s).")
        except Exception as e:
            print("Error clicking 'További termék megjelenítése' buttons:", e)
        html = page.content()
        browser.close()
        return html

