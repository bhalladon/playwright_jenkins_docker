import pytest

from playwright.sync_api import expect
from pom.automation_practise_home_page import *


@pytest.mark.ui
@pytest.mark.usefixtures("page", "navigate")
class TestAutomation:

    def test_verify_url(self, page):
        expect(page).to_have_url("https://testautomationpractice.blogspot.com/")

    def test_fill_data(self, page):
        page.locator(name_text_box).fill("rajiv")
        page.select_option(select_country_from_dropdown, "India")

    def test_alert_button(self,page):
        page.on("dialog", handle_dialog)
        page.locator(simple_alert).click()

    def test_new_tab(self,page):
        with page.context.expect_page() as new_page:
            page.locator(new_tab).click()
        print(new_page.value.url)

