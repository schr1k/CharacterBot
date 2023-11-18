## Setup:
1. Create virtual environment.
```bash
python -m venv venv
```
2. Activate it.
```bash
venv/bin/activate
```
3. Install requirements.
```bash
pip install -r requirements.txt
```

4. Change credentials in config.py.
```python
# Telegram
TOKEN = 'TOKEN'

# Postgres
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'postgres'
POSTGRES_DB = 'Character'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = '5432'

# Redis
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_DB = '3'

# Amplitude
AMPLITUDE_API_KEY = 'AMPLITUDE_API_KEY'
```

## SQL:
1. users
```postgresql
CREATE TABLE users (
    id        SERIAL,
    tg        VARCHAR,
    username  VARCHAR,
    name      VARCHAR,
    surname   VARCHAR,
    time      TIMESTAMP,
    character VARCHAR
)
```
2. characters:
```postgresql
CREATE TABLE characters (
    character   VARCHAR,
    greeting    VARCHAR,
    instruction VARCHAR
);
```
3. messages:
```postgresql
CREATE TABLE messages (
    tg      VARCHAR,
    message VARCHAR
);
```
