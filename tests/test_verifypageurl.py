import time

def test_verify_page_url(page) :
    time.sleep(5)
    assert page.url == "https://www.google.com/"
