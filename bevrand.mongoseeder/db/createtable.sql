CREATE TABLE users
(
    id BIGSERIAL PRIMARY KEY NOT NULL,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(250) NOT NULL,
    email VARCHAR(60),
    active BOOLEAN NOT NULL,
    datecreated TIMESTAMP,
    dateupdated TIMESTAMP
);
CREATE UNIQUE INDEX users_username_uindex ON users (username);