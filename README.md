#  Backend

Developed by:



---

## Technologies

- Python
- Django Framework

---

## URIs and Port Mapping

For local development, the following URIs & ports are used:

| URI            | Port   | Description                                             |
|----------------|--------|---------------------------------------------------------|
| http:localhost | 8000   | Backend is accessible on http://localhost:8000 |


## For Running on your Local Machine (Docker)

- Clone the repository

## Local DB Connection update .env file:

- DB_NAME=sunset_backend_database
- DB_USER=localhost
- DB_PASSWORD=postgres
- DB_HOST=db
- DB_PORT=5432

- you can configure above configurations according to your ease.
---

- Run `docker compose up --build -d` or `docker compose up --build`
- For shutting down the container Run `docker compose down`
- when you'll Run `docker compose up --build -d` or `docker compose up --build` it'll automatically install dependencies for project via requirements.txt file.


### LOCAL DJANGO COMMANDS OPERATIONS ###

- If require to run django commands locally
    - `docker exec -it <container_name> python manage.py createsuperuser`
    - `docker exec -it <container_id> python manage.py migrate`
