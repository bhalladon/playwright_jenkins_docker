import os
import allure
import pytest
from pom.google_home import GoogleHome
from playwright.sync_api import expect


@pytest.mark.skipif("google" not in os.getenv("APP_URL"), reason="Test not running on Google website")
@allure.parent_suite("UI")
@allure.description("Google search test")
def test_google_search(page):
    page.locator(GoogleHome.text_search_box).click()
    page.locator(GoogleHome.text_search_box).fill("hello")
    page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle")
    assert "hello" in page.title().lower()

@allure.parent_suite("UI")
@allure.description("Check page title")
def test_page_tile(page):
    allure.step("Checking page title")
    expect(page).to_have_title("Automation Testing Practice")


@pytest.mark.skip
def test_iframe(page):
    page.locator('//a[.="JavaScript Dialogs"]//following::span[@title="Debugging software licenses"]').click()
    page.wait_for_load_state("networkidle")
    page.frame_locator('iframe[name="aswift_0"]').locator('//a[.="cyara.com"]').click()
    page.wait_for_load_state("networkidle")
