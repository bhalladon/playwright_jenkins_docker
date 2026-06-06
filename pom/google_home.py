# page to store web element locators for google home page

class GoogleHome:

    text_search_box = "//textarea[@name='q']"

    def __init__(self, name):
        self.name = name
        print("Google Home")


    def get_search_textbox(self):
        print(self.name)
        return self.text_search_box


