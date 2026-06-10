import pytest
from playwright.sync_api import Page, expect


@pytest.mark.parametrize("action_to_take", ["continue", "fulfill", "abort"])
def test_mock_network_request(page: Page, action_to_take):
    """
    :param page:
    :param action_to_take: pass a value here for the network interception to take
    example values are : continue, fulfill, abort
    and the default is continued which will just let the request happen as normal
    the action_to_take can be useful for testing how your UI handles slow loading or error states
    for example pass action_to_take="abort" to see how your ui responds to failed api calls
    and pass action_to_take="fulfill" to mock the return data from an api
    and pass action_to_take="continue" to let the api call happen as normal

    :return:
    """

    # create a 255 character long name
    # long_name = ""
    # for i in range(255): long_name += str(random.randint(0, 9))

    # 1. Intercept the fruit API call before navigating
    def handle_route(route):
        if action_to_take.lower() == "continue":
            route.continue_()  # Continue with the original request
        elif action_to_take.lower() == "fulfill":
            mock_data = [{"name": "Rajiv", "id": 1}]
            route.fulfill(json=mock_data)
        elif action_to_take.lower() == "abort":
            route.abort()

    # Register the route handler
    page.route("*/**/api/v1/fruits", handle_route)

    # 2. Navigate to the page
    page.goto("https://demo.playwright.dev/api-mocking/")

    # 3. Assert that your mocked data rendered correctly on the UI
    if action_to_take == "fulfill":
        expect(page.get_by_text("Rajiv")).to_be_visible()

    elif action_to_take == "continue":
        expect(page.get_by_text("Strawberry")).to_be_visible()

    elif action_to_take == "abort":
        expect(page.get_by_text("Loading")).to_be_visible()


def test_mock_network_request_modify_headers(page: Page):
    """
    Intercept and modify headers
    This is useful for testing authentication flows
    or modifying the user agent etc
    or testing mobile vs desktop views
    or testing how your ui responds to different content types
    or testing how your ui responds to different languages
    or testing how your ui responds to different content encodings
    or any other request properties that are sent with the request
    :param page:
    :return:
    """

    def handle_route(route):
        headers = {**route.request.headers, "authorization": "Bearer my-token", "user-agent": "rajiv_chrome"}
        route.continue_(headers=headers)

    page.route("*/**/api/v1/fruits", handle_route)

    with page.expect_response("*/**/api/v1/fruits") as response_info:
        page.goto("https://demo.playwright.dev/api-mocking/")

    sent_headers = response_info.value.request.all_headers()

    assert sent_headers.get("authorization") == "Bearer my-token"
    assert sent_headers.get("user-agent") == "rajiv_chrome"
    expect(page.get_by_text("Strawberry")).to_be_visible()


def test_modify_response_headers(page: Page):
    """
    Intercept and modify response headers
    This is useful for testing how your ui responds to different content types
    or different languages
    or different content encodings
    or any other response properties that are sent with the response
    :param page:
    :return:
    """

    def handle_route(route):
        response = route.fetch()
        modified_headers = {**response.headers, "x-custom-header": "my-custom-value", "content-language": "en-US"}
        route.fulfill(response=response, headers=modified_headers)

    page.route("*/**/api/v1/fruits", handle_route)

    with page.expect_response("*/**/api/v1/fruits") as response_info:
        page.goto("https://demo.playwright.dev/api-mocking/")

    response_headers = response_info.value.headers

    assert response_headers.get("x-custom-header") == "my-custom-value"
    assert response_headers.get("content-language") == "en-US"
    expect(page.get_by_text("Strawberry")).to_be_visible()


def test_replace_response(page:Page):
    """
    Intercept and replace the entire response
    This is useful for testing how your ui responds to different response bodies
    or different status codes
    or different response headers
    or any other response properties that are sent with the response
    or replacing a response with a file
    or replacing a response with a static json response
    or replacing a response with a mock response
    or replacing a response with a response that has a different content type
    :param page:
    :return:
    """
    def handle_route(route):
        route.fulfill(
            status=200,
            headers={
                "content-type": "application/json"
            },
            json=[{
                "name":"Rajiv",
                "id":1
            }]
        )

    page.route("*/**/api/v1/fruits", handle_route)
    page.goto("https://demo.playwright.dev/api-mocking/")
    expect(page.get_by_text("Rajiv")).to_be_visible()



