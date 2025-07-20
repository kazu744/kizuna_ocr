CREATE DATABASE kizuna_ocr;

CREATE USER 'kizuna'@'localhost' IDENTIFIED BY '202310';

GRANT ALL PRIVILEGES ON kizuna_ocr.* TO 'kizuna'@'localhost';

FLUSH PRIVILEGES;

CREATE TABLE users
(id int AUTO_INCREMENT NOT NULL,
 email varchar(255) NOT NULL,
 password varchar(255) NOT NULL,
 created_at datetime NOT NULL,
 updated_at datetime,
 deleted_at datetime,
 PRIMARY KEY (id)
);

CREATE UNIQUE INDEX idx_users_email ON users(email);

CREATE INDEX idx_users_created_at ON users(created_at);

CREATE INDEX idx_users_deleted_at ON users(deleted_at);

CREATE TABLE ocrs
(id int AUTO_INCREMENT NOT NULL,
 user_id int NOT NULL,
 new_owner_name varchar(50),
 new_owner_address_main varchar(50),
 new_owner_address_street varchar(50),
 new_owner_address_number varchar(50),
 raw_text text,
 created_at datetime NOT NULL,
 updated_at datetime,
 deleted_at datetime,
 PRIMARY KEY (id),
 CONSTRAINT fk_ocrs_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_ocrs_user_id ON ocrs(user_id);

CREATE INDEX idx_ocrs_new_owner_name ON ocrs(new_owner_name);

CREATE INDEX idx_ocrs_created_at ON ocrs(created_at);

CREATE INDEX idx_ocrs_deleted_at ON ocrs(deleted_at);