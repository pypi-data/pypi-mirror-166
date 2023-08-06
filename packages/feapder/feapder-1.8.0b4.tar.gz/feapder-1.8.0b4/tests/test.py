from playwright.sync_api import sync_playwright
from playwright.sync_api import Page

driver = sync_playwright().start()
browser = driver.chromium.launch()
page: Page = browser.new_page()
# page.goto("https://baidu.com")
# print(page.context.cookies())
# print(page.evaluate("() => navigator.userAgent"))

print(type(driver), type(browser))