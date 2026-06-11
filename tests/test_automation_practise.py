import pytest

from playwright.sync_api import expect

from pom.automation_practise_home_page import *


@pytest.mark.ui
@pytest.mark.usefixtures("page","navigate")
class TestAutomationPractise:

    @pytest.mark.usefixtures("login")
    @pytest.mark.parametrize("username,password", [("admin", "admin123"), ("user", "user123")])
    def test_login(self, page, username, password):
        expect(page).to_have_url("https://testautomationpractice.blogspot.com/")

    def test_navigation(self, page):
        click_on_tab_section(page, tab_name="Udemy Courses")
        page.wait_for_load_state()

    def test_fill_data(self, page):
        name_locator = page.get_by_role("textbox", name="Enter Name")
        name_locator.click()
        name_locator.fill("Rajiv")
        # page.locator(name_text_box).fill("Rajiv")
        page.locator(email_text_box).fill("rajiv@gmail.com")
        page.locator(phone_text_box).fill("1234567890")
        page.locator(address_text_box).fill("Bangalore")
        page.locator(Gender_radio_button.format("male")).click()
        page.locator(days_checkbox.format("monday")).click()
        page.select_option(select_country_from_dropdown, "India")
        page.select_option(colors_scroll_down_box, "Green")
        page.select_option(animals_list_scroll_down_box, "Rabbit")
        select_date_from_calendar(page, date_to_enter="01/04/2026")  # Enter date in format mm/dd/yyyy
        page.wait_for_load_state()

    def test_alert_button(self, page):
        """
        Test alert button functionality
        :param page:
        :return:
        """
        page.on("dialog", handle_dialog)
        page.locator(simple_alert).click()

    def test_confirmation_alert(self, page):
        page.on("dialog", lambda dialog: dialog.accept())
        page.locator(confirmation_alert).click()

    def test_prompt_alert(self, page):
        page.on("dialog", lambda dialog: dialog.accept("Rajiv"))
        page.locator(prompt_alert).click()

    def test_new_tab(self, page):
        """
        Handle new tab
        opening and switching to it
        :param page:
        :return:
        """

        with page.context.expect_page() as new_page_info:
            page.locator(new_tab).click()

        new_page = new_page_info.value
        new_page.wait_for_load_state()
        print(f"New tab URL: {new_page.url}")

        # Switch back to old tab
        page.bring_to_front()
        print(f"Old tab URL: {page.url}")

        # switch back to new tab
        new_page.bring_to_front()
        print(f"New tab URL: {new_page.url}")

    def test_mouse_hover(self, page):
        mouse_hover_over_element(page, element=mouse_hover)

    def test_scrolling_drop_down(self, page, navigate):
        page.locator(scrolling_drop_down).click()
        page.locator("//div[@id='dropdown']//following::div[@class='option' and .='Item 8']").click()

    def test_price_of_product(self, page):
        # page.context.tracing.start()

        price = get_price_from_the_table(page, product_name="Tablet")
        print(f"Price of Mobile is: {price}")
        # page.context.tracing.stop(path="trace.zip")

    def test_upload_single_file(self, page):
        """
        Test for checking single file upload functionality
        :param page:
        :return:
        """
        page.set_input_files("//input[@id='singleFileInput']", "pytest.ini")
