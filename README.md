# Pytest Playwright Template

This repository provides a template for setting up End-to-End (E2E) tests using Python, Pytest, and Playwright. It includes integrations for reporting, parallel execution, test data generation, and Docker support.

## Features

- **Pytest:** Test runner.
- **Playwright:** Browser automation library.
- **Page Object Model (POM):** Structured way to represent web pages.
- **pytest-html:** Generates HTML test reports.
- **Allure:** Generates detailed Allure test reports.
- **pytest-xdist:** Enables parallel test execution.
- **Faker:** Generates fake data for tests.
- **python-dotenv:** Manages environment variables (e.g., credentials, URLs) via `.env` files.
- **Test Tagging:** Using Pytest markers (`@pytest.mark.<tag>`).
- **Docker Support:** Includes Dockerfiles for running tests and viewing Playwright traces.
- **UV Support:** Instructions for using the UV package manager.

## Prerequisites

- Python (3.8+ recommended)
- Docker (optional, for running tests in containers)
- [UV](https://github.com/astral-sh/uv) (optional, faster alternative to pip/venv)

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd pytest-playwright-template
    ```

2.  **Set up the environment and install dependencies:**

    - **Option A: Using `venv` and `pip` (Standard)**

      ```bash
      # Create a virtual environment
      python -m venv venv

      # Activate the virtual environment
      # On Windows:
      # venv\Scripts\activate
      # On macOS/Linux:
      source venv/bin/activate

      # Install dependencies
      pip install -r requirements.txt
      ```

    - **Option B: Using `uv` (Faster)**
      _(Make sure you have UV installed: `pip install uv` or follow official instructions)_

      ```bash
      # Create and activate a virtual environment using uv
      uv venv
      source .venv/bin/activate # (or .venv\Scripts\activate on Windows)

      # Install dependencies using uv
      uv pip install -r requirements.txt
      ```

3.  **Configure Environment Variables:**

    - Copy the example environment file:
      ```bash
      cp .env.example .env
      ```
    - Edit the `.env` file and add your actual test credentials, base URLs, etc. **Note:** `.env` is included in `.gitignore` and should not be committed to version control.

4.  **Install Playwright Browsers:**
    - Run the following command to download the necessary browser binaries:
      ```bash
      playwright install
      ```
    - To install a single browser (e.g., only Chromium):
      ```bash
      playwright install chromium
      ```
    - You might need system dependencies for the browsers. If the above command fails or you are on Linux, run:
      ```bash
      playwright install --with-deps
      ```

## Directory Structure

```
├── .env.example        # Example environment variables file
├── .gitignore          # Files ignored by git
├── Dockerfile          # Dockerfile for running tests
├── README.md           # This file
├── conftest.py         # Pytest fixtures and hooks
├── pages/              # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py    # Base class for all page objects
│   └── login_page.py   # Example login page object
├── pytest.ini          # Pytest configuration (markers, options)
├── requirements.txt    # Project dependencies
├── data/               # Test data (if needed, e.g., JSON, CSV files)
│   └── __init__.py
├── tests/              # Test scripts
│   ├── __init__.py
│   └── test_login.py   # Example test suite for login functionality
└── utils/              # Utility functions or helper classes
    └── __init__.py
```

## Running Tests

Make sure your virtual environment is activated.

- **Run all tests:**

  ```bash
  pytest
  ```

  This will also generate `report.html` and populate the `allure-results` directory.

- **Run tests with a specific marker:**

  ```bash
  pytest -m smoke
  pytest -m login
  pytest -m "not smoke" # Run all tests except smoke
  ```

- **Run tests in parallel (using available CPU cores):**
  ```bash
  pytest -n auto
  ```
  See pytest-xdist docs: https://pytest-xdist.readthedocs.io/

- **Run tests with Playwright tracing enabled:**
  (Useful for debugging failed tests)

  ```bash
  pytest --tracing on
  ```

  This will generate `trace.zip` files in the `test-results` directory (created automatically if tests fail with tracing on).

- **Pass specific options to Playwright (e.g., run headful):**
  ```bash
  pytest --headed
  ```

## Viewing Reports

- **HTML Report:**

  - Open the generated `report.html` file in your web browser.

- **Allure Report:**

  1.  **Option A: Local Allure Installation**
      - Generate the report (requires [Allure command-line tool](https://docs.qameta.io/allure/#_installing_a_commandline) installed):
        ```bash
        allure generate allure-results --clean
        ```
      - Open the generated report:
        ```bash
        allure open
        ```
  2.  **Option B: Using Docker (Recommended for easy setup)**
      - Run the Allure Docker service container, mounting your local `allure-results` directory. This command pulls the image if you don't have it locally.
        ```bash
        docker run -p 5050:5050 -e CHECK_RESULTS_EVERY_SECONDS=1 -v $(pwd)/allure-results:/app/allure-results frankescobar/allure-docker-service
        ```
      - Open `http://localhost:5050/` in your web browser. The report will be generated automatically and updated if new results appear in `allure-results`.
      - For the latest report, navigate to `http://localhost:5050/allure-docker-service/latest-report`
      - _(Note: If using Docker Desktop on Windows with WSL2, you might need to use the full path or adjust the volume mount syntax accordingly, e.g., `-v //c/Users/YourUser/Projects/pytest-playwright-template/allure-results:/app/allure-results`)_

- **Playwright Trace Viewer:**
  1.  Run tests with `--tracing on` or `--tracing retain-on-failure` (default). Failed tests will generate `trace.zip` files (usually in `test-results/<test_name>/trace.zip`).
  2.  Use the Playwright CLI to view a specific trace:
      ```bash
      playwright show-trace test-results/<path-to-your-test>/trace.zip
      ```

## Using Docker

- **Build the Test Runner Image:**

  ```bash
  docker build -t pytest-runner .
  ```

- **Run Tests in Docker:**

  - Build the image if you haven't already:
    ```bash
    docker build -t pytest-runner .
    ```
  - Run all tests (uses the default `CMD` in Dockerfile):
    ```bash
    docker run --rm pytest-runner
    ```
  - Run all tests, mounting local result directories:
    ```bash
    docker run --rm \
        -v $(pwd)/reports/allure-results:/automation/reports/allure-results \
        -v $(pwd)/reports/test-results:/automation/resports/test-results \
        pytest-runner
    ```
  - Run tests passing the `.env` file (use with caution, prefer injected secrets in CI):
    ```bash
    docker run --rm --env-file .env \
        -v $(pwd)/reports/allure-results:/automation/reports/allure-results \
        -v $(pwd)/reports/test-results:/automation/resports/test-results \
        pytest-runner
    ```
  - **Run a specific test file** inside the container:
    ```bash
    docker run --rm pytest-runner pytest tests/test_login.py
    ```
  - Run tests with a **specific marker** inside the container:
    ```bash
    docker run --rm pytest-runner pytest -m smoke
    ```
  - Run tests in **parallel** inside the container:
    ```bash
    docker run --rm pytest-runner pytest -n auto
    ```
  - _Note: Remember to adjust volume mount paths (`/automation/...`) if you changed the `WORKDIR` in the Dockerfile._
  - _Note: For CI/CD pipelines, prefer injecting secrets as environment variables rather than mounting the `.env` file._


## Configuration

- **Pytest:** Configuration options, markers, and default arguments are defined in `pytest.ini`.
- **Environment Variables:** Sensitive data (credentials, URLs) and environment-specific settings should be stored in a `.env` file (copy from `.env.example`). These are loaded automatically in `conftest.py`.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.
