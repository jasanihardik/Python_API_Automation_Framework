# Python API Automation Framework

REST API automation framework built with Python, Pytest, Requests, schema validation, reusable endpoint clients, data-driven test payloads, reporting, Docker support, and GitHub Actions CI.

The framework uses the public Restful Booker API as the main system under test. It is a good practice API because it supports authentication, create/read/update/delete operations, health checks, request payloads, response validation, and negative testing scenarios.

## Tech Stack

| Area | Tooling |
|---|---|
| Language | Python 3.11+ |
| Test Runner | Pytest |
| HTTP Client | Requests |
| Schema Validation | jsonschema |
| Test Data | JSON files + Faker |
| Config | YAML + environment variables |
| Reporting | pytest-html + Allure |
| CI/CD | GitHub Actions |
| Containerization | Docker |

## Framework Structure

```text
Python_API_Automation_Framework/
├── api/
│   ├── clients/
│   │   └── base_api_client.py
│   ├── endpoints/
│   │   ├── auth_api.py
│   │   ├── booking_api.py
│   │   └── health_check_api.py
│   └── schemas/
│       ├── auth_schema.py
│       └── booking_schema.py
├── config/
│   ├── config.yaml
│   └── config_loader.py
├── data/
│   ├── booking_payloads.json
│   └── invalid_booking_payloads.json
├── docs/
│   └── api_test_strategy.md
├── tests/
│   ├── conftest.py
│   └── api/
│       ├── test_auth_api.py
│       ├── test_booking_api.py
│       ├── test_booking_negative.py
│       ├── test_booking_workflow.py
│       └── test_health_check_api.py
├── utils/
│   ├── assertions.py
│   ├── data_generator.py
│   ├── logger.py
│   └── schema_validator.py
├── .github/workflows/api-tests.yml
├── Dockerfile
├── Makefile
├── pytest.ini
├── requirements.txt
└── .env.example
```

## What This Framework Demonstrates

- Reusable API client design
- Endpoint abstraction similar to Page Object Model for UI automation
- Authentication and token-based API workflows
- CRUD API validation
- Positive, negative, contract, smoke, regression, and workflow tests
- JSON schema validation for response contracts
- Data-driven test payloads
- Dynamic test data generation
- Request/response logging
- Pytest fixtures for clean setup and teardown
- HTML and Allure reporting
- GitHub Actions pipeline execution
- Dockerized test execution

## API Under Test

Base URL:

```text
https://restful-booker.herokuapp.com
```

Main endpoints covered:

| Endpoint | Purpose |
|---|---|
| `GET /ping` | Health check |
| `POST /auth` | Create auth token |
| `GET /booking` | Get booking IDs |
| `GET /booking/{id}` | Get booking details |
| `POST /booking` | Create booking |
| `PUT /booking/{id}` | Full update booking |
| `PATCH /booking/{id}` | Partial update booking |
| `DELETE /booking/{id}` | Delete booking |

## Local Setup

Clone the repository:

```bash
git clone https://github.com/jasanihardik/Python_API_Automation_Framework.git
cd Python_API_Automation_Framework
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

For Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run all tests:

```bash
pytest
```

Run only API tests:

```bash
pytest -m api
```

Run smoke tests:

```bash
pytest -m smoke
```

Run regression tests:

```bash
pytest -m regression
```

Run negative tests:

```bash
pytest -m negative
```

## Reports

Generate a pytest HTML report:

```bash
pytest --html=reports/api_test_report.html --self-contained-html
```

Generate Allure results:

```bash
pytest --alluredir=reports/allure-results
```

Serve Allure report locally:

```bash
allure serve reports/allure-results
```

## Environment Configuration

Default environment is `demo`.

```bash
API_ENV=demo pytest
```

The framework reads configuration from:

```text
config/config.yaml
```

Optional environment overrides can be added using a local `.env` file. Keep `.env` out of Git.

Example:

```bash
cp .env.example .env
```

## Docker Execution

Build the Docker image:

```bash
docker build -t python-api-automation-framework .
```

Run tests inside Docker:

```bash
docker run --rm python-api-automation-framework
```

Run tests and mount local reports folder:

```bash
docker run --rm -v "$(pwd)/reports:/app/reports" python-api-automation-framework
```

## Makefile Commands

```bash
make install
make test
make smoke
make regression
make negative
make html-report
make allure-results
```

## GitHub Actions

The workflow is located at:

```text
.github/workflows/api-tests.yml
```

It runs on pull requests and pushes to `main`. The workflow installs dependencies, runs tests, and uploads the HTML report as a build artifact.

## Test Design

The tests are organized by intent:

| Test File | Focus |
|---|---|
| `test_health_check_api.py` | Availability and smoke validation |
| `test_auth_api.py` | Token generation and auth validation |
| `test_booking_api.py` | Booking endpoint CRUD coverage |
| `test_booking_negative.py` | Invalid IDs and unauthorized operations |
| `test_booking_workflow.py` | End-to-end API workflow validation |

## Notes

The public API can occasionally be slow or temporarily unavailable. Timeout, logging, and clear assertions are included to make failures easier to troubleshoot in local and CI runs.
