# Rate limiter
---

## Description
Rate limiter is a sample project that implements a rate limiting alongside with testing.

---

## Get Started
Clone the repo using `git clone https://github.com/erfan-rfmhr/rate-limiter.git`.
Change directory to the project using `cd rate-limiter`.
To start the project using uv:
- Install uv using `pip install uv`.
- Install the project dependencies using `uv sync`.
- Migrate the database using `uv run python manage.py migrate`.
- Start the project using `uv run python manage.py runserver`.

Using pip:
- Create a virtual environment using `python -m venv .venv`.
- Activate the virtual environment using `source .venv/bin/activate` in linux/macOS or `venv\Scripts\activate` in windows.
- Install the project dependencies using `pip install -r requirements.txt`.
- Migrate the database using `python manage.py migrate`.
- Start the project using `python manage.py runserver`.

## Architecture
The code follows `fat models, skinny views` architecture. Views are responsible for handling requests and responses, logic is handled by serializers and models.

### Configuration
All configurations and variables are stored in `config/` such as settings and url dispatch.

### Structure
The apps are created based on business domain. For example, `accounts` app is responsible for account and user management.

Each app looks like this:

```
accounts/
├── __init__.py
├── admin.py
├── api/
│   ├── __init__.py
│   └── v1/
│       ├── __init__.py
│       ├── serializers/
│       │   ├── __init__.py
│       │   └── wallets.py
│       ├── urls.py
│       └── views/
│           ├── __init__.py
│           └── wallets.py
├── apps.py
├── migrations/
│   ├── 0001_initial.py
│   ├── 0002_alter_wallet_user.py
│   └── __init__.py
├── models/
│   ├── __init__.py
│   ├── users.py
│   └── wallets.py
├── signals/
│   ├── __init__.py
│   └── users.py
└── tests.py
```
Key notes:
- Semantic versioning is used for APIs under `api/<version>`.
- All APIs are openapi formatted documented in `schema/`.
- Components of each domain (for example users and wallets) are grouped in their own files.

### Throttling
Throttling rates are defined in `config/settings.py` as `DEFAULT_THROTTLE_RATES`.
Limitation is set for logical APIs; `api/v1/accounts/wallets/deposit` and `api/v1/accounts/wallets/withdraw` in this case.

### Logging
API logs are stored in `api_request.log` file.
For every request, an INFO‌ message is logged with the request details.
For every throttled request, an ERROR message is logged with the request details.

### Testing
The `tests.py` file in each app contains tests.
In this case, the rate limiting test is implemented in `accounts/tests.py`.
The test checks:
- A user allows to perform requests 5 times in 60 seconds.
- After 5 requests, the user is throttled by the 6th request and their requests are rejected until the next 60 seconds.
- The limitation is reset after 60 seconds.
- Users do not affect on each other's limitation.

### Exception Handling
A custom exception handler is implemented in `config/exception_handler.py` in order to support more django core exceptions and provide complete responses.

### Documenting
All APIs are documented in openapi format.
The documentation is available at `/schema`, `/schema/swagger-ui` and `/schema/redoc`.