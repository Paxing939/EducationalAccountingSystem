CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL
);

INSERT INTO students (name, age) VALUES
('Alice', 23),
('Bob', 21);
