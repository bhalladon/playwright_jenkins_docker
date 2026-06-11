"""
Page object model for home page
"""

home_locator = '//div[@id="crosscol"]//li/a[.="{}"]'
name_text_box = "//input[@id='name']"
email_text_box = "//input[@id='email']"
phone_text_box = "//input[@id='phone']"
address_text_box = "//label[.='Address:']//following::textarea[@id='textarea']"
Gender_radio_button = "//input[@name='gender' and @type='radio' and @id='{}']"
days_checkbox = "//input[@type='checkbox' and @value='{}']"
select_country_from_dropdown = "//select[@id='country']"
colors_scroll_down_box = "//label[.='Colors:']//following::select[@id='colors']"
animals_list_scroll_down_box = "//label[.='Sorted List:']//following::select[@id='animals']"
date_picker_1 = "//input[@id='datepicker']"
previous_button_date_picker = "//a[@class='ui-datepicker-prev ui-corner-all']"
current_selected_year_on_calendar = "//span[@class='ui-datepicker-year']"
current_selected_month_on_calendar = "//span[@class='ui-datepicker-month']"
select_date_calendar = "//a[@data-date='{}']"
simple_alert = "//button[.='Simple Alert']"
confirmation_alert = "//button[.='Confirmation Alert']"
prompt_alert = "//button[.='Prompt Alert']"
new_tab = "//button[.='New Tab']"
mouse_hover = "//button[.='Point Me']"
scrolling_drop_down = "//input[@id='comboBox']"
total_page_count_product_table = "//ul[@id='pagination']//child::li"


def handle_dialog(dialog):
    print(f"Dialog message: {dialog.message}")
    assert dialog.message == "I am an alert box!", f"Dialog message not matching, actual dialog message is {dialog.message}"
    dialog.accept()


def click_on_tab_section(page, tab_name):
    page.locator(home_locator.format(tab_name)).click()


def select_date_from_calendar(page, date_to_enter: str):
    """
    This function will help to enter date in date picker calendar
    :param page:
    :param date_to_enter: enter in format mm/dd/yyyy for e.g. to enter 4th january 1983, please enter 04/01/1983
    :return:
    """
    # fabricate date, month and year from date_to_enter
    year = date_to_enter.split("/")[2]
    month = date_to_enter.split("/")[0]
    date = int(date_to_enter.split("/")[1].lstrip('0'))

    month_mapping_to_actual_month_name = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December"}

    if month not in month_mapping_to_actual_month_name.keys():
        raise Exception("Month should be between 1 and 12")
    if date not in range(1, 32):
        raise Exception("Day should be between 1 and 31")
    if len(year) != 4:
        raise Exception("Year should be 4 digit number")

    # First select the year from the calendar
    # check current year on the calendar
    page.locator(date_picker_1).click()
    current_selected_year = page.locator(current_selected_year_on_calendar).text_content()
    if int(current_selected_year) > int(year):
        # click on previous button till we reach the required year
        while int(current_selected_year) != int(year):
            page.locator(previous_button_date_picker).click()
            current_selected_year = page.locator(current_selected_year_on_calendar).text_content()
            mouse_hover_over_element(page, mouse_hover)
            if int(current_selected_year) == int(year):
                if page.locator(current_selected_month_on_calendar).text_content() == month:
                    break
    elif int(current_selected_year) == int(year):
        # check for month on the calendar
        if page.locator(current_selected_month_on_calendar).text_content() != month_mapping_to_actual_month_name.get(month):
            # click on previous button till we reach the required month
            while page.locator(current_selected_month_on_calendar).text_content() != month_mapping_to_actual_month_name.get(month):
                page.locator(previous_button_date_picker).click()
                mouse_hover_over_element(page, mouse_hover)
                if page.locator(current_selected_month_on_calendar).text_content() == month_mapping_to_actual_month_name.get(month):
                    break

    # select date from the calendar
    mouse_hover_over_element(page, select_date_calendar.format(date))
    page.locator(select_date_calendar.format(date)).click()


def mouse_hover_over_element(page, element):
    """
    Hover over an element
    :param element:
    :param page:
    :return:
    """
    page.locator(element).hover()


def get_price_from_the_table(page, product_name):
    """
    Get price of a product from the table
    :param page:
    :param product_name: name of the product
    :return: price of the product
    """
    # count the number of pages available
    total_number_of_pages_in_table = page.locator(total_page_count_product_table).count()
    for i in range(1, total_number_of_pages_in_table + 1):
        # count the number of rows available
        number_of_rows_in_table = page.locator("//table[@id='productTable']//child::tbody/tr").count()
        for j in range(1, number_of_rows_in_table + 1):
            product_name_from_row = page.locator(
                f"//table[@id='productTable']//child::tbody/tr[{j}]/td[2]").text_content()
            if product_name_from_row.strip() == product_name.strip():
                price_of_product = page.locator(
                    f"//table[@id='productTable']//child::tbody/tr[{j}]/td[3]").text_content()
                return price_of_product
        # Check if this is last page of the table or not
        # if yes then return from the function
        if total_number_of_pages_in_table - i == 1:
            print("Product not found in the table")
            return None
        # navigate to next page of the table
        page.locator(f"//ul[@id='pagination']//child::li//a[.='{i + 1}']").click()
    return None
