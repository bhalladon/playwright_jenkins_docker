import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from api.api_client import ApiClient

load_dotenv()

APP_URL = os.getenv("APP_URL")

@pytest.fixture()
def page(browser, request):
    page = browser.new_page()
    yield page
    try:
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            page.screenshot(path=f"screenshots/{request.node.name}.png", full_page=True)
    finally:
        page.close()


@pytest.fixture()
def navigate(page):
    page.goto(APP_URL)
    page.wait_for_load_state("networkidle")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture()
def browser():
    browser_name = os.getenv("WEB_BROWSER", "chrome")
    headless = os.getenv("HEADLESS", "false").lower() == "true"
    args = ["--start-maximized"]

    browser_map = {
        "chrome": lambda p: p.chromium.launch(headless=headless, channel="chrome", args=args),
        "edge": lambda p: p.chromium.launch(headless=headless, channel="msedge", args=args),
        "firefox": lambda p: p.firefox.launch(headless=headless, args=args),
        "webkit": lambda p: p.webkit.launch(headless=headless, args=args),
    }

    with sync_playwright() as p:
        browser = browser_map.get(browser_name, lambda p: p.chromium.launch(headless=headless, args=args))(p)
        context = browser.new_context(no_viewport=True)
        context.set_default_timeout(30000)
        yield context
        context.close()


@pytest.fixture(scope="function")
def login(username, password):
    print("login successful with", username, password)


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and before performing collection and entering the run test loop.
    """
    print("\n--- Pytest session started ---")
    # Perform global setup tasks, e.g., connecting to a database


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finishes, right before returning the exit status to the system.
    """
    print("\n--- Pytest session finished ---")
    # Perform global teardown tasks, e.g., closing database connections


def pytest_addoption(parser):
    """
        Register argparse-style options and ini-style config values,
        called once at the beginning of a test run.
        """
    parser.addoption(
        "--env", action="store", default="prod", help="Environment to run tests against (e.g., dev, staging, prod)"
    )
    parser.addoption(
        "--runslow", action="store", default="false", help="Environment to run tests against (e.g., dev, staging, prod)"
    )
    # You can then access this option in your tests or other hooks using
    # request.config.getoption("--env").


def pytest_configure(config):
    """
       Called after command line options have been parsed and all plugins have been loaded.
       """
    if config.getoption("--env") == "dev":
        print("Running tests in PRODUCTION environment!")
        # Apply specific configurations for production


def pytest_runtest_setup(item):
    """
    Called before pytest_runtest_call().
    """
    print(f"\nSetting up for test: {item.name}")


def pytest_runtest_call(item):
    """
    Called to execute the test item.
    """
    print(f"Executing test: {item.name}")


def pytest_runtest_teardown(item, nextitem):
    """
    Called after pytest_runtest_call().
    """
    print(f"Tearing down after test: {item.name}")


def pytest_collection_modifyitems(config, items):
    """
    Called after test collection has been performed.
    """
    for item in items:
        if "slow" in item.keywords.node.name and not config.getoption("--runslow"):
            print("Skipping Test")
            item.add_marker(pytest.mark.skip(reason="need --runslow option to run"))


@pytest.fixture(scope="session")
def api_client():
    return ApiClient()
