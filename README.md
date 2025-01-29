# HouseworkTracker

# Setup

Create the database using the create.sql file:
`psql -f create.sql`

Add a .env file in the root directory. This needs to contain the following data (replacing with the correct details):
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_SERVER=server
POSTGRES_PORT=1234
POSTGRES_DB=housework
