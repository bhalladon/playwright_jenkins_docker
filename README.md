# Playwright Test Automation Framework

A Python-based test automation framework using **Playwright** with **UI** and **API** test coverage, integrated with **Jenkins**, **Docker**, and **GitHub Actions CI/CD**, with **Allure** reporting.

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
│   ├── test_automation_practise.py  # UI tests
│   └── test_api.py                  # API tests
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

Create a `.env` file in the project root (already provided):

```env
WEB_BROWSER=chrome
APP_URL=https://testautomationpractice.blogspot.com/
HEADLESS=true
API_BASE_URL=https://jsonplaceholder.typicode.com
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

### Run with Allure reporting
```bash
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

### Run with a specific browser
Set `WEB_BROWSER` in `.env` or pass it as an env variable:
```bash
WEB_BROWSER=firefox pytest tests/ -v
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

| Fixture / Hook | Scope | Description |
|---|---|---|
| `browser` | session | Launches browser (chrome/firefox/edge/webkit) |
| `page` | function | Opens a new page, navigates to APP_URL, auto-screenshots on failure |
| `api_client` | session | Returns a shared `ApiClient` instance |
| `open_app_url` | function | Navigates to APP_URL |
| `pytest_runtest_makereport` | hook | Enables failure detection for screenshot capture |
| `pytest_addoption` | hook | Adds `--env` and `--runslow` CLI options |

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

> Set `APP_URL` as a GitHub repository secret for use in CI.

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
