CREATE DATABASE housework;
CREATE USER housework_admin WITH ENCRYPTED PASSWORD 'housework';
GRANT ALL PRIVILEGES ON DATABASE housework TO housework_admin;
GRANT CREATE ON SCHEMA public TO housework_admin;
GRANT USAGE ON SCHEMA public TO housework_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO housework_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO housework_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO housework_admin;

CREATE TYPE priority AS ENUM ('LOW', 'MEDIUM', 'HIGH');
CREATE TABLE users (
        id SERIAL NOT NULL, 
        name VARCHAR(50) NOT NULL, 
        email VARCHAR NOT NULL, 
        active BOOLEAN, 
        PRIMARY KEY (id), 
        UNIQUE (email)
);