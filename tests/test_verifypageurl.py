import pytest

@pytest.mark.skip
def test_verify_page_url(page) :
    assert page.url == "https://www.google.com/"
