CREATE DATABASE housework;
CREATE USER housework_admin WITH ENCRYPTED PASSWORD 'housework';
GRANT ALL PRIVILEGES ON DATABASE housework TO housework_admin;