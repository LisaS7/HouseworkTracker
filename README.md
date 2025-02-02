# HouseworkTracker

## Features

- **Task Management**: Create, update, and delete tasks.
- **Tagging**: Assign tags to tasks for better organization.
- **User Management**: Manage users who are responsible for tasks.
- **API Endpoints**: A RESTful API built with FastAPI to manage tasks and users.

## Tech Stack

- **Backend**: FastAPI (Python web framework)
- **Database**: PostgreSQL (via SQLAlchemy ORM)
- **Containerization**: Docker
- **Testing**: pytest for unit and integration tests

## Installation (to run on localhost)

### Prerequisites

Make sure you have the following installed:

- **Python 3.12+**
- **Docker** (if using containers)
- **PostgreSQL** (if running the database locally)

### Setting Up the Development Environment

1. Clone the repository:

   ```bash
   git clone https://github.com/LisaS7/HouseworkTracker.git
   cd HouseworkTracker
   ```

2. Set up a virtual environment and install the dependencies:

```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

3. Create the database using the create.sql file:
   `psql -f DB/create.sql`

4. Add a .env file in the root directory. This needs to contain the following data (replacing with the correct details):

```
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_SERVER=server
POSTGRES_PORT=1234
POSTGRES_DB=housework
```

5. Start the application:

`uvicorn app.main:app --reload`

This will start the development server on http://127.0.0.1:8000.

### Docker

Alternatively, after cloning the repository, run in a docker container with the provided Dockerfile:

```
docker build -t houseworktracker:latest .
docker run -d --name houseworktracker -p 8000:8000 houseworktracker:latest
```
