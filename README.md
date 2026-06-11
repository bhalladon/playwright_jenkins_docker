# Playwright Test Automation Framework

A Python-based test automation framework using **Playwright** with **UI** and **API** test coverage, integrated with **Jenkins**, **Docker**, and **GitHub Actions CI/CD**, with **Allure** reporting and **Slack** notifications.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Programming language |
| Playwright 1.60 | Browser automation |
| pytest 9.x | Test runner |
| requests | API testing |
| Allure | Test reporting |
| Docker | Containerized test execution |
| Jenkins | CI/CD pipeline |
| GitHub Actions | Cloud CI/CD |
| python-dotenv | Environment config management |
| Slack | Build notifications |

---

## Project Structure

```
playwright_jenkins_docker/
├── .github/workflows/
│   └── playwright_tests.yml     # GitHub Actions CI workflow
├── api/
│   └── api_client.py            # Reusable API client (GET, POST, PUT, DELETE)
├── pom/
│   └── automation_practise_home_page.py  # Page Object Model (locators + helpers)
├── screenshots/                 # Auto-captured screenshots on test failure
├── tests/
│   ├── test_automation_practise.py       # UI tests (class-based)
│   ├── test_api.py                       # API tests
│   └── test_network_intercept.py         # Network interception tests
├── .env                         # Local environment variables
├── conftest.py                  # pytest fixtures and hooks
├── Dockerfile                   # Docker image for containerized runs
├── Jenkinsfile                  # Jenkins declarative pipeline
├── pytest.ini                   # pytest markers configuration
└── requirements.txt             # Python dependencies
```

---

## Setup & Installation

### Prerequisites
- Python 3.12+
- pip

### Install dependencies

```bash
pip install -r requirements.txt
playwright install chrome
```

### Configure environment

Create a `.env` file in the project root for local test execution:

```env
WEB_BROWSER="chrome"
APP_URL="https://testautomationpractice.blogspot.com/"
APP_URL_FOR_NETWORK_INTERCEPT_TESTS="https://demo.playwright.dev/api-mocking/" # For Testing network intercept
HEADLESS="true"
API_BASE_URL="https://jsonplaceholder.typicode.com"
```

---

## Running Tests

### Run all tests
```bash
pytest tests/ -v
```

### Run only UI tests
```bash
pytest tests/ -m ui -v
```

### Run only API tests
```bash
pytest tests/ -m api -v
```

### Run only Network Intercept tests
```bash
pytest tests/ -m network_intercept -v
```

### Run with Allure reporting
```bash
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

### Run with a specific browser
Set `WEB_BROWSER` in `.env`, pass it as an env variable, or use the `--web_browser` CLI option:
```bash
WEB_BROWSER=firefox pytest tests/ -v
# or
pytest tests/ --browser=firefox -v
```
Supported browsers: `chrome`, `firefox`, `edge`, `webkit`

### Run in headed mode
```bash
HEADLESS=false pytest tests/ -v
```

---

## pytest Markers

Defined in `pytest.ini`:

| Marker | Description |
|---|---|
| `ui` | UI / browser tests |
| `api` | API tests |
| `smoke` | Smoke test suite |
| `e2e` | End-to-end test suite |
| `network_intercept` | Network interception tests |

---

## Test Suites

### UI Tests — `tests/test_automation_practise.py`
Target: https://testautomationpractice.blogspot.com/

| Test | Description |
|---|---|
| `test_login` | Parametrized login with multiple credentials |
| `test_navigation` | Tab navigation |
| `test_fill_data` | Form fill (text, radio, checkbox, dropdown, date picker) |
| `test_alert_button` | Simple alert handling |
| `test_confirmation_alert` | Confirmation dialog handling |
| `test_prompt_alert` | Prompt dialog with input |
| `test_new_tab` | New tab open and switch |
| `test_mouse_hover` | Mouse hover interaction |
| `test_scrolling_drop_down` | Custom scrollable dropdown |
| `test_price_of_product` | Multi-page table data extraction |
| `test_upload_single_file` | Single file upload |

### API Tests — `tests/test_api.py`
Target: https://jsonplaceholder.typicode.com

| Test | Description |
|---|---|
| `test_get_all_posts` | GET /posts — validates 100 records |
| `test_get_single_post` | GET /posts/1 — validates response body |
| `test_create_post` | POST /posts — validates 201 Created |
| `test_update_post` | PUT /posts/1 — validates updated fields |
| `test_delete_post` | DELETE /posts/1 — validates 200 OK |

### Network Intercept Tests — `tests/test_network_intercept.py`
Target: https://demo.playwright.dev/api-mocking/

| Test | Description |
|---|---|
| `test_mock_network_request[continue]` | Lets the real API request proceed, asserts real data is rendered |
| `test_mock_network_request[fulfill]` | Mocks API response with custom JSON, asserts mocked data is rendered |
| `test_mock_network_request[abort]` | Aborts the API request, asserts UI shows loading/error state |
| `test_mock_network_request_modify_headers` | Intercepts request and injects custom `authorization` and `user-agent` headers |
| `test_modify_response_headers` | Fetches real response then re-fulfills it with modified response headers |
| `test_replace_response` | Replaces entire API response with a static JSON payload |

---

## Page Object Model

`pom/automation_practise_home_page.py` contains:
- All XPath locators as module-level constants
- Helper functions: `click_on_tab_section`, `select_date_from_calendar`, `mouse_hover_over_element`, `get_price_from_the_table`, `handle_dialog`

---

## API Client

`api/api_client.py` provides a session-based reusable HTTP client:

```python
api_client.get("/posts")
api_client.post("/posts", payload)
api_client.put("/posts/1", payload)
api_client.delete("/posts/1")
```

Base URL is loaded from `API_BASE_URL` in `.env`.

---

## conftest.py — Fixtures & Hooks

| Fixture / Hook                  | Scope | Description |
|---------------------------------|---|---|
| `web_browser`                   | session | Launches a browser context (chrome/firefox/edge/webkit), no viewport, 30s default timeout; reads from `WEB_BROWSER` env var or `--web_browser` CLI option |
| `page`                          | function | Opens a new page, auto-screenshots on failure |
| `navigate`                      | function | Navigates the current page to `APP_URL` and waits for `networkidle` |
| `api_client`                    | session | Returns a shared `ApiClient` instance |
| `login`                         | function | Stub fixture for login setup (prints credentials) |
| `pytest_runtest_makereport`     | hook | Enables failure detection for screenshot capture |
| `pytest_addoption`              | hook | Adds `--env`, `--web_browser`, and `--runslow` CLI options |
| `pytest_configure`              | hook | Applies env-specific configuration based on `--env` value |
| `pytest_sessionstart`           | hook | Called before test collection; used for global setup |
| `pytest_sessionfinish`          | hook | Called after test run; used for global teardown |
| `pytest_runtest_setup`          | hook | Called before each test |
| `pytest_runtest_call`           | hook | Called during each test execution |
| `pytest_runtest_teardown`       | hook | Called after each test |
| `pytest_collection_modifyitems` | hook | Skips tests marked `slow` unless `--runslow` is passed |

---

## Docker

Build and run tests inside a Docker container:

```bash
# Build the image
docker build -t playwright-tests .

# Run tests
docker run playwright-tests
```

The Dockerfile:
- Uses `python:3.12-slim`
- Installs Java 21 + Allure CLI
- Installs Python dependencies and Playwright Chrome
- Runs pytest with Allure report generation on container start

Default env vars baked into the image:
```
WEB_BROWSER=chrome
HEADLESS=true
APP_URL=https://testautomationpractice.blogspot.com/
```

---

## Jenkins Pipeline

The `Jenkinsfile` defines a declarative pipeline with:

**Parameters (configurable per build):**
- `WEB_BROWSER` — chrome / firefox / edge
- `TEST_TYPE` — ALL / UI / API
- `PYTEST_MARKER` — custom marker expression (e.g. `smoke`, `api`)

**Stages:**
1. `Linux Tasks` — installs dependencies and Playwright browsers (Linux agents)
2. `Windows Tasks` — installs dependencies and Playwright browsers (Windows agents)
3. `Run Tests` — executes pytest with selected options and generates Allure results

**Post actions:**
- Archives `screenshots/*.png` as build artifacts
- Publishes Allure HTML report via the Allure Jenkins plugin
- Sends Slack notification to `#qa-demo` — ✅ success, ❌ failure, ⚠️ unstable

### Jenkins Slack Setup

1. Install the **Slack Notification Plugin** — `Manage Jenkins → Plugins`
2. Go to `Manage Jenkins → System → Slack`:
   - Set your Slack **Workspace** name
   - Add credential — Kind: `Secret text`, Secret: your `xoxb-...` Bot Token, ID: `slack-token`
   - Set default channel: `#qa-demo`
3. Invite the bot to your Slack channel: `/invite @<your-bot-name>`

**Slack message includes:** job name, build number, browser, test type, and a direct link to the build.

---

## GitHub Actions

Workflow file: `.github/workflows/playwright_tests.yml`

Triggers:
- Push to `main`
- Pull request to `main`
- Manual dispatch with inputs (browser, test type, marker)

Steps:
1. Checkout code
2. Set up Python 3.x
3. Install dependencies
4. Install Playwright browsers with system deps
5. Run pytest with Allure results
6. Upload screenshots on failure as artifacts
7. Generate Allure report
8. Deploy Allure report to **GitHub Pages** (`gh-pages` branch), keeping last 20 reports
9. Send Slack notification with build status, branch, browser, actor, and run URL

### GitHub Actions Slack Setup

1. Go to https://api.slack.com/apps → select your app → **Incoming Webhooks** → toggle ON
2. Click **"Add New Webhook to Workspace"** → select your channel → **Allow**
3. Copy the webhook URL: `https://hooks.slack.com/services/T.../B.../xxx...`
4. Validate the webhook locally before adding to GitHub:
```bash
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Hello from GitHub Actions!"}' \
  https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```
5. Add it as a GitHub repository secret:
   - Repo → `Settings → Secrets and variables → Actions → New repository secret`
   - Name: `SLACK_WEBHOOK_URL`, Value: your webhook URL

**Required GitHub Secrets:**

| Secret | Description |
|---|---|
| `APP_URL` | Target UI test URL |
| `API_BASE_URL` | Target API base URL |
| `SLACK_WEBHOOK_URL` | Slack Incoming Webhook URL for notifications |

**Slack message includes:** build status, workflow name, branch, browser, triggered-by actor, and a direct link to the Actions run.

---

## Screenshots

Automatically captured to `screenshots/` on test failure, named after the test function (e.g. `test_fill_data[chrome].png`).

---

## Requirements

```
pytest~=9.0.3
requests~=2.34.2
pytest-xdist~=3.6.1
playwright~=1.60.0
python-dotenv~=1.2.2
allure-pytest~=2.16.0
```
