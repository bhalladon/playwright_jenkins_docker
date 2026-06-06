import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()


@pytest.fixture(scope="function")
def page(browser, request):
    page = browser.new_page()
    page.goto(os.getenv("APP_URL"))
    page.wait_for_load_state("networkidle")
    yield page
    # Add screenshot feature on failed tests
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        page.screenshot(path=f"screenshots/{request.node.name}.png", full_page=True)
    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="session", params=["chrome", "firefox"])
def browser(request):
    # browser_name = request.param
    browser_name = os.getenv("WEB_BROWSER")
    headless = os.getenv("HEADLESS", "false").lower() == "true"

    with sync_playwright() as p:
        args = ["--start-maximized"]
        if browser_name == "chrome":
            browser = p.chromium.launch(headless=headless, channel="chrome", args=args)
        elif browser_name == "edge":
            browser = p.chromium.launch(headless=headless, channel="msedge", args=args)
        elif browser_name == "webkit":  # Safari browser
            browser = p.webkit.launch(headless=headless, args=args)
        elif browser_name == "firefox":
            browser = p.firefox.launch(headless=headless, args=args)
        else:
            browser = p.chromium.launch(headless=headless)
        context = browser.new_context(no_viewport=True)
        context.set_default_timeout(30000)
        yield context
        context.close()


@pytest.fixture(scope="function")
def open_app_url(page):
    page.goto(os.getenv("APP_URL"))


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
